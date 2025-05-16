"""FastAPI application to generate a CV using Gemini API and LaTeX templates."""

import re
import logging
import json
import google.generativeai as genai
from jinja2 import Environment, FileSystemLoader
from pydantic import BaseModel
from fastapi import FastAPI


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


# Define expected input
class UserQuery(BaseModel):
    """Model for user input."""

    prompt: str


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
Extract the following fields from the user's self-description:
- name
- location
- email
- phone
- linkedin
- github
- website
- education (list with degree, university, years, gpa, coursework)
- work experience (list with job_title, company, location, years, bullet_points)
Return as a JSON object.
User input:
\"\"\"
{{ prompt }}
\"\"\"
"""


@app.post("/generate-cv/")
async def generate_cv(user_query: UserQuery):
    """Endpoint to generate a CV based on user input."""
    response = model.generate_content(
        EXTRACTION_PROMPT.replace("{{ prompt }}", user_query.prompt)
    )
    # Get structured data from the model
    structured_data = clean_json_string(response.text)

    try:

        data = json.loads(structured_data)
    except json.JSONDecodeError:
        return {"error": "Model returned malformed JSON", "raw": structured_data}

    logger.info("Structured data: %s", data)

    # Render LaTeX CV
    rendered_cv = latex_template.render(**data)

    # Save to file
    with open("output/cv.tex", "w", encoding="utf-8") as f:
        f.write(rendered_cv)

    return {"message": "CV generated successfully", "latex": rendered_cv}


def clean_json_string(model_output: str) -> str:
    """Cleans model output by removing Markdown-style formatting and fixing single quotes."""
    # Remove Markdown-style backticks and 'json' label
    cleaned_output = re.sub(
        r"```json\s*|\s*```", "", model_output.strip(), flags=re.MULTILINE
    )

    # Convert single quotes to double quotes to make it valid JSON
    cleaned_output = cleaned_output.replace("'", '"')

    return cleaned_output
