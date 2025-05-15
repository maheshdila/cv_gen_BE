from fastapi import FastAPI, HTTPException, Request, File, UploadFile
import fitz  # PyMuPDF
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
    education: List[Any]
    experience: List[Any]
    projects: List[Any]
    skills: Any
    achievements: List[Any]
    contact: Any
    desired_role: str = "Software Engineer"

class

# === Helper to build prompt ===
def build_prompt(data: CVData):
    PROMPT = f"""
    Extract the following information from the input text and return it in a JSON format:

    - Full Name
    - Email
    - Phone Number
    - Location
    - Education (degree, university, graduation year, GPA, courses)
    - Work Experience (company, role, responsibilities)
    - Skills (languages, technologies)
    - LinkedIn URL
    - GitHub URL
    - Interests or hobbies

    Input:
    \"\"\"{USER_INPUT}\"\"\"
    """

    # === Generate Response ===
    response = model.generate_content(PROMPT)
    return response


# === POST Endpoint ===
@app.post("/generate-cv")
async def generate_cv(cv_data: CVData):
    try:
        prompt = build_prompt(cv_data)
        response = model.generate_content(prompt)
        return {"generated_cv": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# === Run Server (if needed) ===
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


@app.post("/extract-text/")
async def extract_text(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        return {"error": "Please upload a PDF file"}

    contents = await file.read()

    from io import BytesIO

    text = ""
    pdf_stream = BytesIO(contents)
    with fitz.open(stream=pdf_stream, filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()

    return {"filename": file.filename, "extracted_text": text}
