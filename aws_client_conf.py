import boto3
import os
import requests


def aws_client(region: str, service: str):
    if os.getenv('ACCESS_KEY') and os.getenv('SECRET_KEY'):
        print("Executing with Access and Secret key")
        ec2 = boto3.client(service,
                           aws_access_key_id=os.getenv('ACCESS_KEY'),
                           aws_secret_access_key=os.getenv('SECRET_key'),
                           region_name=region
                           )
        return ec2
    elif check_iam_role_exists() is True:
        print("Executing with IAM Role")
        ec2 = boto3.client('ec2', region_name=region)
        return ec2
    else:
        print("=============== Please use either IAM role or ACCESS and SECRET keys===============")


def check_iam_role_exists():
    req = requests.get('http://169.254.169.254/latest/meta-data/iam/security-credentials')
    if req.status_code == requests.status_codes.codes.ok:
        return True
    else:
        return False
