# myapp/s3_security_check.py

import boto3
from django.conf import settings

AWS_ACCOUNT_NUMBER = settings.AWS_ACCOUNT_NUMBER
AWS_REGION = settings.AWS_REGION

def perform_s3_bucket_security_check():
    # Create an S3Control client
    s3control_client = boto3.client("s3control", region_name=AWS_REGION)

    # Get the current public access block configuration for the account
    response = s3control_client.get_public_access_block(AccountId=AWS_ACCOUNT_NUMBER)

    public_access_block_config = response["PublicAccessBlockConfiguration"]

    # Perform the security check based on the public access block configuration
    block_public_acls = public_access_block_config["BlockPublicAcls"]
    ignore_public_acls = public_access_block_config["IgnorePublicAcls"]
    block_public_policy = public_access_block_config["BlockPublicPolicy"]
    restrict_public_buckets = public_access_block_config["RestrictPublicBuckets"]

    if block_public_acls and ignore_public_acls and block_public_policy and restrict_public_buckets:
        status = "PASS"
        status_extended = f"Block Public Access is configured for the account {AWS_ACCOUNT_NUMBER}."
    else:
        status = "FAIL"
        status_extended = f"Block Public Access is not configured for the account {AWS_ACCOUNT_NUMBER}."

    # You can return the results or handle them as needed
    return {
        "status": status,
        "status_extended": status_extended,
        "resource_id": AWS_ACCOUNT_NUMBER,
        "region": AWS_REGION,
    }
