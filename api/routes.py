# === app/api/routes.py ===
from fastapi import APIRouter,Depends
from models.user import UserQuery
from services.cv_service import generate_cv_from_user
from auth.token_verifier_utility import verify_token

router = APIRouter()

@router.post("/generate-cv/")
async def generate_cv(user_input: UserQuery):
    return await generate_cv_from_user(user_input)

@router.get("/test")
def api_test(user=Depends(verify_token)):
    return {"message": "FastAPI server is running..."}