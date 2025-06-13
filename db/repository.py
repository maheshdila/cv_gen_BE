from db.dynamodb import table

def save_user_data(email: str,data:dict):
    table.put_item(Item={"email":email, **data})

def get_user_data(email:str):
    response = table.get_item(Key={"email":email})
    return response.get("Item")
