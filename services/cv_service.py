# === app/services/cv_service.py ===
from cv_gen_BE.core.langgraph_pipeline import graph_executor
from cv_gen_BE.models.user import UserQuery
#from app.db.repository import save_user_data

async def generate_cv(user_input: UserQuery):
    input_data = {"raw_input": user_input.dict(exclude_none=True)}
    try:
        result = graph_executor.invoke(input_data)
        return {
            "message": result.get("message", "Success"),
            "latex": result.get("latex"),
            "pdf_path":result.get("pdf_path"),
            "s3_url": result.get("s3_url")
        }
    except Exception as e:
        return {"error": str(e)}


#from chatgpt

async def generate_cv_from_user(user_input):
    input_dict = {"raw_input": user_input.dict(exclude_none=True)}
    result = graph_executor.invoke(input_dict)

    email = user_input.other_bio_data.get("email", "anonymous")
    save_user_data(email, result)

    return {
        "message": result.get("message", "Success"),
        "latex": result.get("latex"),
        "pdf_path": result.get("pdf_path"),
        "s3_url": result.get("s3_url")
    }


