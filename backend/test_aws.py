import boto3
import os

# Fetch credentials from environment variables
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_DEFAULT_REGION = os.getenv('AWS_DEFAULT_REGION')

print(AWS_ACCESS_KEY_ID)

# Initialize the S3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_DEFAULT_REGION
)

try:
    # List the buckets to test if the credentials are valid
    response = s3_client.list_buckets()
    print("S3 Buckets:")
    for bucket in response['Buckets']:
        print(f"  {bucket['Name']}")
except Exception as e:
    print(f"Error: {e}")