# === app/api/routes.py ===
from fastapi import APIRouter
from models.user import UserQuery
from services.cv_service import generate_cv_from_user

router = APIRouter()

@router.post("/generate-cv/")
async def generate_cv(user_input: UserQuery):
    return await generate_cv_from_user(user_input)

@router.get("/test")
def api_test():
    return {"message": "FastAPI server is running..."}