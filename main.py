"""FastAPI application to generate a CV using Gemini API and LaTeX templates."""

import re
import logging
import json
import subprocess
from typing import Optional, Dict, List, Union
from jinja2 import Environment, FileSystemLoader
import google.generativeai as genai
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


logger = logging.getLogger("uvicorn.error")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

# import openai


# === Gemini API Key and Setup ===
API_KEY = "AIzaSyB9jeDjHFp319jUiiBNaibr4KPrn9ylpDY"  # Replace with your actual API key
genai.configure(api_key=API_KEY)

# === Choose the Gemini Model ===
model = genai.GenerativeModel("gemini-2.0-flash")


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can also specify a list like ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class UserQuery(BaseModel):
    name: Optional[str] = None
    other_bio_data: Optional[Dict[str, str]] = None
    summary: Optional[str] = None
    education: Optional[Union[str, List[Dict[str, str]]]] = None
    work_experience: Optional[Union[str, List[Dict[str, str]]]] = None
    skills: Optional[Union[str, List[str]]] = None
    certifications: Optional[Union[str, List[str]]] = None
    projects: Optional[Union[str, List[Dict[str, str]]]] = None


env = Environment(
    loader=FileSystemLoader("templates"),
    block_start_string="((*",
    block_end_string="*))",
    variable_start_string="(((",
    variable_end_string=")))",
    comment_start_string="((#",
    comment_end_string="#))",
)

latex_template = env.get_template("basic.tex")


# Load your Gemini/GPT API key
# openai.api_key = os.getenv("OPENAI_API_KEY")

# # Load your LaTeX template (can be loaded from a file instead)
# with open("templates/basic.tex", "r", encoding="utf-8") as f:
#     latex_template = Template(f.read())

# Gemini/GPT Prompt for extracting structured data
EXTRACTION_PROMPT = """
Extract the following fields from this partially structured user input. If a field is already structured (e.g., a list or dict), keep it as-is. Otherwise, extract it cleanly:

- name
- email
- phone
- linkedin
- github
- summary
- education (list with degree, university, years, gpa, coursework)
- work_experience (list with job_title, company, location, years, bullet_points)
- skills (list)
- certifications (list)
- projects (list with name, link, description)

User input:
```json
{{ input_json }}
"""


@app.post("/generate-cv/")
async def generate_cv(user_input: UserQuery):
    """Endpoint to generate a CV from partially structured input."""

    # Serialize input to JSON string
    input_json = json.dumps(user_input.dict(exclude_none=True), indent=2)

    # Format and send to Gemini
    prompt = EXTRACTION_PROMPT.replace("{{ input_json }}", input_json)
    response = model.generate_content(prompt)
    structured_data = clean_json_string(response.text)

    try:
        data = json.loads(structured_data)
    except json.JSONDecodeError:
        return {"error": "Malformed JSON", "raw": structured_data}

    logger.info("Structured data: %s", data)

    # Render LaTeX
    rendered_cv = latex_template.render(**data)

    with open("output/cv.tex", "w", encoding="utf-8") as f:
        f.write(rendered_cv)

    # Compile LaTeX to PDF
    compile_latex()

    return {"message": "CV generated", "latex": rendered_cv}


def compile_latex():
    try:
        subprocess.run(["LaTeXCompiler", "-file", "cv.tex"], cwd="output", check=True)
        print("Compilation successful.")
    except subprocess.CalledProcessError as e:
        print("Compilation failed:", e)


def clean_json_string(model_output: str) -> str:
    """Cleans model output by removing Markdown-style formatting and fixing single quotes."""
    # Remove Markdown-style backticks and 'json' label
    cleaned_output = re.sub(
        r"```json\s*|\s*```", "", model_output.strip(), flags=re.MULTILINE
    )

    # Convert single quotes to double quotes to make it valid JSON
    cleaned_output = cleaned_output.replace("'", '"')

    return cleaned_output
