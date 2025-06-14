from db.dynamodb import table

def save_user_data(email: str,data:dict):
    table.put_item(Item={"email":email, **data})

def get_user_data(email:str):
    response = table.get_item(Key={"email":email.strip()})
    return response.get("Item")

def update_latest_raw_input(email: str, new_raw_input: str,update_time:str) -> dict:

    resp = table.update_item(
        Key={"email": email},
        UpdateExpression="SET raw_input = :ri, created_at = :ca",
        ExpressionAttributeValues={
            ":ri": new_raw_input,
            ":ca": update_time,
        },
        ReturnValues="UPDATED_NEW"
    )
    return resp.get("Attributes", {})