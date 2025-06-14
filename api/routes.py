# === app/api/routes.py ===
from fastapi import APIRouter, Query
from models.user import UserQuery
from services.cv_service import generate_cv_from_user
from services.user_service import user_query_save, get_cv_by_user_email

router = APIRouter()

@router.post("/generate-cv/")
async def generate_cv(user_input: UserQuery):
    return await generate_cv_from_user(user_input)

@router.post("/queries-save")
async def create_query(payload: UserQuery):
    print("message received")
    return await user_query_save(payload)

@router.get("/queries-get")
async def get_cv_by_email(email: str = Query(..., description="User email")):
    return await get_cv_by_user_email(email)

@router.get("/test")
def api_test():
    return {"message": "FastAPI server is running..."}