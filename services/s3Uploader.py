from datetime import datetime
from typing import Dict, Any
import boto3
from botocore.exceptions import NoCredentialsError

def upload_to_s3_agent(pdf_path : str) ->dict:
    # pdf_path = state["pdf_path"]
    # email = state["ats_optimized_data"].get("email", "anonymous")
    # safe_email_hash = "demo"
    # timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    s3_key = pdf_path
    bucket_name = "cv-bucket-protfolio-app"
    region_name = "ap-southeast-1"

    s3_client = boto3.client("s3", region_name=region_name)

    try:
        # Upload the file
        s3_client.upload_file(pdf_path, bucket_name, s3_key)
        print(f"File uploaded to s3://{bucket_name}/{s3_key} in region {region_name}")

        # Generate pre-signed URL with content headers
        presigned_url = s3_client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': bucket_name,
                'Key': s3_key,
                'ResponseContentType': 'application/pdf',
                'ResponseContentDisposition': 'inline'
            },
            ExpiresIn=3600
        )
        return {"s3_url": presigned_url}
    except FileNotFoundError:
        return {"error": f"Error: PDF file not found at {pdf_path}"}
    except NoCredentialsError:
        return {"error": "Error: AWS credentials not found. Make sure IAM role is attached."}
    except Exception as e:
        return {"error": f"Error uploading to S3: {str(e)}"}