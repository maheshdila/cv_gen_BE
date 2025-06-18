# === app/api/routes.py ===
from fastapi import APIRouter, Query, Depends
from models.user import UserQuery
# from services.cv_service import generate_cv_from_user
from services.user_service import user_query_save, get_cv_by_user_email, update_latest_raw_input
from auth.token_verifier_utility import verify_token
from workflows.cv_automation.crew import CVAutomationWorkflow

router = APIRouter()

# @router.post("/generate-cv/")
# async def generate_cv(user_input: UserQuery,user: dict = Depends(verify_token)):
#     email = user_input.formData.personalDetails["email"]
#     return await generate_cv_from_user(user_input, email)

@router.post("/generate-cv-typst/")
async def generate_cv_types(user_input: UserQuery):
    print("message received")
    try:
        email = user_input.formData.personalDetails["email"]
        await user_query_save(user_input, email)
        workflow = CVAutomationWorkflow()
        final_result = workflow.run(user_input, "my-cv-bucket")
        # print(f"Success! CV URL: {final_result['final_cv_url']}")
        print(f"Success! final result: {final_result}")
        return {"message": "Success!", "final_result": final_result}
    except Exception as ex:
        print(f"Error: {ex}")
        return {"error": f"Error: {ex}"}


@router.post("/queries-save")
async def create_query(payload: UserQuery,user: dict = Depends(verify_token)):
    print("message received")
    email = payload.formData.personalDetails["email"]
    return await user_query_save(payload,email)

@router.get("/queries-get")
async def get_cv_by_email(email: str = Query(..., description="User email")
                          ,user: dict = Depends(verify_token)):
    return await get_cv_by_user_email(email)

@router.put("/query-update")
async def update_query(payload: UserQuery,user: dict = Depends(verify_token)):
    return await update_latest_raw_input(payload)

@router.get("/test")
def api_test(user=Depends(verify_token)):
    return {"message": "FastAPI server is running..."}