from datetime import datetime
from botocore.exceptions import ClientError
from fastapi import HTTPException
from fastapi import status

from db.dynamodb import table

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
        "email": "sample@email",   # partition key
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