from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import google.generativeai as genai
import json
import uvicorn
from typing import Any, List


# === CONFIG ===
API_KEY = "AIzaSyB9jeDjHFp319jUiiBNaibr4KPrn9ylpDY"  # Replace with your actual key

# === SETUP ===
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

# === FASTAPI APP ===
app = FastAPI()

# === Pydantic Model ===

class CVData(BaseModel):
    biography: str
    education:List[Any]
    experience: List[Any]
    projects: List[Any]
    skills: Any
    achievements:List[Any]
    contact:Any
    desired_role: str = "Software Engineer"

# === Helper to build prompt ===
def build_prompt(data: CVData):
    prompt = (
        "You are a professional resume writer. The user has shared the following details:\n\n"
        f"Bio: {data.biography}\n\n"
        f"Work Experience: {json.dumps(data.experience, indent=2)}\n\n"
        f"Projects: {json.dumps(data.projects, indent=2)}\n\n"
        f"The user wants to apply for the role of {data.desired_role}.\n\n"
        "Generate a tailored, ATS-friendly CV for this role."
    )
    return prompt

# === POST Endpoint ===
@app.post("/generate-cv")
async def generate_cv(cv_data: CVData):
    try:
        prompt = build_prompt(cv_data)
        response = model.generate_content(prompt)
        return {"generated_cv": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#=== Run Server (if needed) ===
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
