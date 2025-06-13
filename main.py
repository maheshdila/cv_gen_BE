#
# from models.user import UserQuery
# from core.langgraph_pipeline import graph_executor
# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from services.cv_service import generate_cv
#
# app = FastAPI()
#
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
#
#
# @app.post("/generate-cv/")
#
#
#
#
#
#
# @app.get("/test")
# def api_test():
#     return {"fast api server is up and running..."}

# === app/main.py ===
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from cv_gen_BE.api.routes import router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)