import boto3

ACCESS_KEY = "your-access-key"
SECRET_KEY = "your-secret-key"
REGION_NAME = "your-region"


def get_aws_resource(res_name):
    session = boto3.Session(
        region_name=REGION_NAME,
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
    )
    return session.resource(res_name)


def get_aws_client(client_name):
    session = boto3.Session(
        region_name=REGION_NAME,
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
    )
    return session.client(client_name)
