from datetime import datetime
from botocore.exceptions import ClientError
from fastapi import HTTPException
from fastapi import status

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
        "raw_query": raw_input,
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
        items = get_user_data(email)
        if not items:
            raise HTTPException(status_code=404, detail="No records found")
        # Extract only the raw_query field and return
        return [item["raw_query"] for item in items]
    except HTTPException:
        # propagate 404s
        raise
    except Exception as e:
        # convert any other errors into a 500
        raise HTTPException(status_code=500, detail=str(e))