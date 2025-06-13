# === app/services/cv_service.py ===
from cv_gen_BE.core.langgraph_pipeline import graph_executor
from cv_gen_BE.models.user import UserQuery
from cv_gen_BE.db.repository import save_user_data
from cv_gen_BE.db.dynamodb import table

#from app.db.repository import save_user_data

async def generate_cv_from_user(user_input: UserQuery):
    input_data = {"raw_input": user_input.dict(exclude_none=True)}
    try:
        response = table.table_status  # Lazy call to check connectivity
        print(f"DynamoDB table status: {response}")
    except Exception as db_check_error:
        return {"error": f"DynamoDB not reachable: {str(db_check_error)}"}
    try:
        #result = graph_executor.invoke(input_data)
        result = {"message":"demo message","latex":"demo latex", "pdf path": "demo path","s3_url":"s3 url demo" }
        email = user_input.other_bio_data.get("email", "anonymous")
        save_user_data(email, result)
        return {
            "message": result.get("message", "Success"),
            "latex": result.get("latex"),
            "pdf_path":result.get("pdf_path"),
            "s3_url": result.get("s3_url")
        }
    except Exception as e:
        return {"error": str(e)}


#from chatgpt

# async def generate_cv_from_user(user_input):
#     input_dict = {"raw_input": user_input.dict(exclude_none=True)}
#     result = graph_executor.invoke(input_dict)
#
#     email = user_input.other_bio_data.get("email", "anonymous")
#     save_user_data(email, result)
#
#     return {
#         "message": result.get("message", "Success"),
#         "latex": result.get("latex"),
#         "pdf_path": result.get("pdf_path"),
#         "s3_url": result.get("s3_url")
#     }
#

