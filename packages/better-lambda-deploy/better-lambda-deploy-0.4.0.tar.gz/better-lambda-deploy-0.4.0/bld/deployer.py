from .function import LambdaFunction, QueueFunction
from .api_function import APIFunction
from jinja2 import Environment, FileSystemLoader
import os
import subprocess
import boto3
import shutil
from zipfile import ZipFile
from io import BytesIO
import json
from .queue import Queue


class Deployer(object):
    def __init__(
        self,
        name,
        dir,
        docker=False,
        environment="prod",
        local=False,
        subdomain=None,
        domain="alexwiss.com",
        pool_id="us-east-1_RIZE20fug",
        certificate_id="6ed4866c-16dd-4db8-81cf-fb1316227679",
    ):
        self.dir = dir
        script_dir = os.path.dirname(os.path.realpath(__file__))
        self.jinja = Environment(loader=FileSystemLoader(script_dir))
        self.project_name = name
        self.environment = environment
        self.docker = docker
        self.local = local
        self.subdomain = subdomain
        self.domain = domain
        self.pool_id = pool_id
        self.certificate_id = certificate_id
        client = boto3.client("sts")
        self.account_id = client.get_caller_identity()["Account"]

        # Appending the current path to grab any other files.
        os.sys.path.append(self.dir)

    def _get_env_vars(self):
        # Getting environment variables.
        env_vars = []
        for name, value in os.environ.items():
            if name[0:4] == "BLD_":
                env_vars.append(
                    {
                        "name": name[4:],
                        "alpha_name": name[4:].replace("_", ""),
                        "value": value,
                        "type": "String",
                    }
                )
        return env_vars

    def _get_queues(self):
        """
        Determine queues based on classes that inherit form bld.Queue.
        """
        queues = []
        for child in Queue.__subclasses__():
            print(child.__name__)
            queues.append({"name": child.__name__.lower()})
        return queues

    def _get_queue_functions(self):
        functions = []
        classes = QueueFunction.__subclasses__()
        for lambda_class in classes:
            if lambda_class.__name__ not in ["APIFunction", "QueueFunction"]:
                functions.append(
                    {"name": lambda_class.__name__, "queue": lambda_class.queue}
                )
        return functions

    def _install_reqs(self):
        reqs = os.path.abspath(f"{self.dir}/requirements.txt")
        subprocess.run(["pip", "install", "-r", reqs], check=True)

    def _build_template(self, output_dir=None):
        # Checking custom output directory.
        output_file = f"{output_dir}/bld.yml" if output_dir else "bld.yml"

        # Installing requirements so everything is importable.
        # self._install_reqs()

        # Running files to create subclasses.
        # TODO: Change these from hardcoded to dynamic.
        exec(open("queues.py").read())
        exec(open("function.py").read())
        exec(open("api.py").read())

        # Get all Lambda Functions.
        lambda_functions = []
        lambda_classes = LambdaFunction.__subclasses__()
        for lambda_class in lambda_classes:
            if lambda_class.__name__ not in ["APIFunction", "QueueFunction"]:
                lambda_functions.append({"name": lambda_class.__name__})

        # Get all APIFunctions.
        api_functions = []
        api_classes = APIFunction.__subclasses__()
        for api in api_classes:
            inst = api()
            methods = inst.get_methods()
            api_functions.append(
                {"name": api.__name__, "endpoint": api.endpoint, "methods": methods}
            )

        # Creating SAM template.
        template = self.jinja.get_template("sam.j2")

        env_vars = self._get_env_vars()
        queues = self._get_queues()

        queue_functions = self._get_queue_functions()

        rendered = template.render(
            description="Test",
            functions=lambda_functions,
            api_functions=api_functions,
            environment_variables=env_vars,
            dynamo_tables=[],
            project_name=self.project_name,
            subdomain=self.subdomain,
            domain=self.domain,
            queues=queues,
            queue_functions=queue_functions,
            pool_id=self.pool_id,
            certificate_id=self.certificate_id,
            account_id=self.account_id,
        )
        f = open(output_file, "w")
        f.write(rendered)
        f.close()

    def _local_build(self):
        build_path = os.path.abspath(f"{self.dir}/.aws-sam/build")
        if os.path.exists(build_path):
            shutil.rmtree(build_path)

        os.makedirs(build_path, exist_ok=True)

        # Install requirements.
        pip_cmd = ["pip", "install", "-r", "requirements.txt", "-t", build_path]
        subprocess.run(pip_cmd, cwd=self.dir)

        # Copy template in there.
        shutil.copyfile("bld.yml", f"{build_path}/template.yml")

        # Copying Python code to build directory.
        # TODO: Add symlinks for all Python files so live updated works.
        for (dirpath, dirnames, filenames) in os.walk(self.dir):
            files = list(filter(lambda x: x.endswith(".py"), filenames))
            break

        for f in files:
            shutil.copyfile(os.path.abspath(f"{dirpath}/{f}"), f"{build_path}/{f}")

    def _sam_build(self):
        # Run the SAM CLI to build and deploy.
        sam_build = ["sam", "build", "--debug", "--template-file", "bld.yml"]
        if self.docker:
            sam_build.append("--use-container")
        subprocess.run(sam_build, cwd=self.dir, check=True)

    def _build(self):
        if self.local:
            self._local_build()
        else:
            self._sam_build()

    def deploy(self):
        self._build_template()

        # Creating S3 bucket for SAM.
        # TODO: Set this to create a random bucket if the name is taken or something.
        s3 = boto3.client("s3")
        s3.create_bucket(
            ACL="private", Bucket=f"{self.project_name}-bld-{self.environment}"
        )
        self._build()
        env_vars = self._get_env_vars()
        overrides = [
            f"ParameterKey={x['alpha_name']},ParameterValue={x['value']}"
            for x in env_vars
        ]
        sam_deploy = [
            "sam",
            "deploy",
            "--stack-name",
            f"{self.project_name}-bld-{self.environment}",
            "--capabilities",
            "CAPABILITY_NAMED_IAM",
            "--s3-bucket",
            f"{self.project_name}-bld-{self.environment}",
            "--template-file",
            ".aws-sam/build/template.yml",
            "--parameter-overrides",
            f"ENVIRONMENT={self.environment}",
        ]
        if len(overrides) > 0:
            sam_deploy.append(",".join(overrides))
        subprocess.run(sam_deploy, cwd=self.dir, check=True)

        print("Deployed successfully.")

    def start_api(self):
        self._build_template()
        self._build()

        env_vars = self._get_env_vars()
        overrides = [f"{x['alpha_name']}={x['value']}" for x in env_vars]
        overrides.append("ENVIRONMENT=sam")

        queues = self._get_queues()
        queue_functions = self._get_queue_functions()
        localstack_endpoint = "http://localhost:4566"
        iam = boto3.client("iam", endpoint_url=localstack_endpoint)
        sqs = boto3.client("sqs", endpoint_url=localstack_endpoint)
        lamb = boto3.client("lambda", endpoint_url=localstack_endpoint)

        # Deploy queues to localstack.
        for queue in queues:
            print(f"Deploying queue {queue['name']}.")
            _ = sqs.create_queue(QueueName=f"legoon-{queue['name']}-prod")

        try:
            role = iam.create_role(
                RoleName="lambda",
                AssumeRolePolicyDocument=json.dumps(
                    {
                        "Version": "2012-10-17",
                        "Statement": [
                            {
                                "Effect": "Allow",
                                "Principal": {"Service": "lambda.amazonaws.com"},
                                "Action": "sts:AssumeRole",
                            }
                        ],
                    }
                ),
            )
            print(role)
        except Exception:
            print("Role exists.")

        try:
            _ = iam.put_role_policy(
                RoleName="lambda",
                PolicyName="allow",
                PolicyDocument=json.dumps(
                    {
                        "Version": "2012-10-17",
                        "Statement": [
                            {"Effect": "Allow", "Action": "*", "Resource": "*"},
                            {"Effect": "Allow", "Action": "logs:*", "Resource": "*"},
                            {
                                "Effect": "Allow",
                                "Action": ["logs:CreateLogStream", "logs:PutLogEvents"],
                                "Resource": ["*"],
                            },
                        ],
                    }
                ),
            )
        except Exception as e:
            print(e)
            print("Role and policy already connected.")

        # Deploy lambda functions
        # Create a ZipFile object
        zip_file = BytesIO()
        with ZipFile(zip_file, "w") as zip_obj:
            # Iterate over all the files in directory
            for folder_name, subfolders, filenames in os.walk(
                f"{self.dir}/.aws-sam/build"
            ):
                for filename in filenames:
                    # Create complete filepath of file in directory
                    file_path = os.path.join(folder_name, filename)
                    arc_path = os.path.join(
                        folder_name.replace(".aws-sam/build", ""), filename
                    )
                    # Add file to zip
                    zip_obj.write(file_path, arcname=arc_path)

        with open("test.zip", "wb") as f:
            f.write(zip_file.getbuffer())
        environment = {
            "Variables": {"ENVIRONMENT": "sam", "AWS_DEFAULT_REGION": "us-east-1"}
        }
        for function in queue_functions:
            print(f"Creating/updating function {function['name']}.")
            # Try to update the function.
            try:
                zip_file.seek(0)
                lamb.update_function_configuration(
                    FunctionName=function["name"], Environment=environment
                )
                lamb.update_function_code(
                    FunctionName=function["name"], Publish=True, ZipFile=zip_file.read()
                )

            except Exception as e:
                print(e)
                print("Function can't be updated. Creating.")
                zip_file.seek(0)
                # If it doesn't exist, create it.
                lamb.create_function(
                    FunctionName=function["name"],
                    Runtime="python3.8",
                    Handler=f"function.{function['name']}Handler",
                    Code={"ZipFile": zip_file.read()},
                    Role="arn:aws:iam::000000000000:role/lambda",
                    Environment=environment,
                )

            try:
                _ = lamb.create_event_source_mapping(
                    EventSourceArn=f"arn:aws:sqs:us-east-1:000000000000:{function['queue']}",
                    FunctionName=function["name"],
                    Enabled=True,
                    BatchSize=10,
                )
            except Exception as e:
                print(e)
                print("Event mapping already deployed.")

        sam_start = [
            "sam",
            "local",
            "start-api",
            "-d 5858",
            "--template-file",
            ".aws-sam/build/template.yml",
            "--docker-network",
            "development_private",
        ]
        if len(overrides) > 0:
            sam_start.append("--parameter-overrides")
            sam_start.append(",".join(overrides))

        subprocess.run(sam_start, cwd=self.dir, check=True)

    def invoke(self, function):
        self._build_template()
        self._build()
        subprocess.run(["sam", "local", "invoke", function], cwd=self.dir, check=True)
