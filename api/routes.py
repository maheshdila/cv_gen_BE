# === app/api/routes.py ===
<<<<<<< HEAD
from fastapi import APIRouter,Depends
from models.user import UserQuery
from services.cv_service import generate_cv_from_user
from auth.token_verifier_utility import verify_token
=======
from fastapi import APIRouter, Query
from models.user import UserQuery
from services.cv_service import generate_cv_from_user
from services.user_service import user_query_save, get_cv_by_user_email, update_latest_raw_input
>>>>>>> d3ef8517dfd75e23d974ce72bd7d7a24f4d11a2b

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

@router.put("/query-update")
async def update_query(payload: UserQuery):
    return await update_latest_raw_input(payload)

@router.get("/test")
def api_test(user=Depends(verify_token)):
    return {"message": "FastAPI server is running..."}