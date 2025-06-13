# === langgraph_cv_pipeline.py ===
import boto3
from langgraph.graph import StateGraph, END
from pydantic import BaseModel
from typing import Dict, Any
import google.generativeai as genai
from jinja2 import Environment, FileSystemLoader
import subprocess
import json
import re

import os
from datetime import datetime
import hashlib
import subprocess

from models.user import UserQuery
from core.langgraph_pipeline import graph_executor








# === FastAPI App ===
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, List, Union

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/generate-cv/")
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





@app.get("/test")
def api_test():
    return {"fast api server is up and running..."}
