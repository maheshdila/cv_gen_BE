import boto3
import os

REGION = os.getenv("AWS_REGION","ap-southeast-1")
session = boto3session=boto3.session.Session()
dynamodb = session.resource("dynamodb",region_name=REGION)
table = dynamodb.Table("CVUserData")