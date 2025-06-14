from datetime import datetime
from botocore.exceptions import ClientError
from fastapi import HTTPException
from fastapi import status
from boto3.dynamodb.conditions import Key
from db.dynamodb import table
from db.repository import get_user_data


async def user_query_save(payload):
    now = datetime.utcnow().isoformat()
    raw_input = payload.dict(exclude={"email"}, exclude_none=True)

    if not payload.other_bio_data or 'email' not in payload.other_bio_data:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Email not provided in other_bio_data"
        )
    email = payload.other_bio_data['email']

    item = {
        "email": email,   # partition key
        "created_at": now,             # sort key
        "raw_input": raw_input,
    }
    # Checked up to this point
    try:
        table.put_item(Item=item)
    except ClientError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save to DynamoDB: {e.response['Error']['Message']}"
        )

    return {"message": "Query saved", "created_at": now}


async def get_cv_by_user_email(email: str):
    """
    Fetches all raw_query strings for the given email.
    """
    try:
        item = get_user_data(email)
        if not item:
            raise HTTPException(status_code=404, detail="No records found")
        # Extract only the raw_query field and return
        return item["raw_input"]
        # return item
    except HTTPException:
        # propagate 404s
        raise
    except Exception as e:
        # convert any other errors into a 500
        raise HTTPException(status_code=500, detail=str(e))


def get_latest_created_at(email: str) -> str:
    resp = table.query(
        KeyConditionExpression=Key("email").eq(email),
        ScanIndexForward=False,  # descending on sort key
        Limit=1
    )
    items = resp.get("Items", [])
    return items[0]["created_at"] if items else None

async def update_latest_raw_input(payload) -> dict:
    email = payload.other_bio_data['email']
    latest = get_latest_created_at(email)
    if not latest:
        raise ValueError("No existing record to update")
    now = datetime.utcnow().isoformat()
    resp = table.update_item(
        Key={"email": email, "created_at": latest},
        UpdateExpression="SET raw_input = :ri, created_at = :ca",
        ExpressionAttributeValues={
            ":ri": payload,
            ":ca": now
        },
        ReturnValues="UPDATED_NEW"
    )
    return resp.get("Attributes", {})
