import boto3
from botocore.config import Config


class Amazon:
    def __init__(self):
        self.aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
        self.aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        self.aws_region = os.getenv("AWS_REGION")
        self.config = Config(signature_version="s3v4")

    def get_textract_resource(self):
        return boto3.resource(
            "textract",
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            region_name=self.aws_region,
            config=self.config,
        )
