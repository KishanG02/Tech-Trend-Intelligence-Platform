from pathlib import Path
import boto3

# MinIO Configuration
MINIO_ENDPOINT = "http://localhost:9000"
ACCESS_KEY = "admin"
SECRET_KEY = "password123"
BUCKET_NAME = "ai-trend-lake"

# Create S3 Client
s3 = boto3.client(
    "s3",
    endpoint_url=MINIO_ENDPOINT,
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
)

# Test file
test_file = Path("test.txt")

with open(test_file, "w") as f:
    f.write("MinIO connection successful!")

# Upload
s3.upload_file(
    str(test_file),
    BUCKET_NAME,
    "test.txt"
)

print("✅ File uploaded successfully!")

# List objects
response = s3.list_objects_v2(
    Bucket=BUCKET_NAME
)

print("\nObjects in bucket:")

for obj in response.get("Contents", []):
    print("-", obj["Key"])