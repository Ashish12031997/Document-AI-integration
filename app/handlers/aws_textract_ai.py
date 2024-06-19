import os

import boto3
from botocore.config import Config
from botocore.exceptions import NoCredentialsError, PartialCredentialsError


class Amazon:
    def __init__(self):
        self.aws_access_key_id = os.getenv("AWS_ACCESS_KEY")
        self.aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        self.aws_region = os.getenv("AWS_REGION")
        self.config = Config(signature_version="s3v4")

    def get_s3_client(self):
        return boto3.client(
            "s3",
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            region_name=self.aws_region,
            config=self.config,
        )

    def upload_file_to_s3(self, file_name: str, bucket_name: str, file_data: bytes):
        s3_client = self.get_s3_client()
        try:
            # Upload the file
            s3_client.put_object(Bucket=bucket_name, key=file_name, body=file_data)
            print(f"File '{file_name}' uploaded to '{bucket}/{object_name}'")
            return True
        except FileNotFoundError:
            print("The file was not found")
            return False
        except NoCredentialsError:
            print("Credentials not available")
            return False
        except PartialCredentialsError:
            print("Incomplete credentials provided")
            return False
        except Exception as e:
            print(f"An error occurred: {e}")
            return False
