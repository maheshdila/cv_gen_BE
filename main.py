# === langgraph_cv_pipeline.py ===

from langgraph.graph import StateGraph, END
from pydantic import BaseModel
from jinja2 import Template, Environment, FileSystemLoader
import os
import re

# import openai

import google.generativeai as genai

# === Gemini API Key and Setup ===
API_KEY = "AIzaSyB9jeDjHFp319jUiiBNaibr4KPrn9ylpDY"  # Replace with your actual API key
genai.configure(api_key=API_KEY)

# === Choose the Gemini Model ===
model = genai.GenerativeModel("gemini-2.0-flash")


app = FastAPI()


# Define expected input
class UserQuery(BaseModel):
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

data = {
    "name": "Samith Perera",
    "email": "samith@example.com",
    "degree": "BSc in Computer Science",
    "university": "University of Colombo",
}


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
    # Ask Gemini or GPT to extract data
    # completion = openai.ChatCompletion.create(
    #     model="gpt-4",  # or Gemini API call
    #     messages=[
    #         {"role": "system", "content": "You are a CV extractor bot."},
    #         {
    #             "role": "user",
    #             "content": EXTRACTION_PROMPT.replace("{{ prompt }}", user_query.prompt),
    #         },
    #     ],
    # )
    response = model.generate_content(
        EXTRACTION_PROMPT.replace("{{ prompt }}", user_query.prompt)
    )
    # Get structured data from the model
    structured_data = clean_json_string(response.text)

    try:
        import json

        data = json.loads(structured_data)
    except json.JSONDecodeError:
        return {"error": "Model returned malformed JSON", "raw": structured_data}

    # Render LaTeX CV
    rendered_cv = latex_template.render(**data)

    # Save to file
    with open("output/cv.tex", "w", encoding="utf-8") as f:
        f.write(rendered_cv)

    return {"message": "CV generated successfully", "latex": rendered_cv}


# === LangGraph Setup ===
class CVState(BaseModel):
    raw_input: dict
    extracted_data: dict = None
    ats_optimized_data: dict = None
    latex_code: str = None


workflow = StateGraph(state_schema=CVState)
workflow.add_node("extract", extract_structured_agent)
workflow.add_node("ats_optimize", ats_optimization_agent)
workflow.add_node("render", render_cv_agent)
workflow.set_entry_point("extract")
workflow.add_edge("extract", "ats_optimize")
workflow.add_edge("ats_optimize", "render")
workflow.add_edge("render", END)

graph_executor = workflow.compile()

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


class UserQuery(BaseModel):
    name: Optional[str] = None
    other_bio_data: Optional[Dict[str, str]] = None
    summary: Optional[str] = None
    education: Optional[Union[str, List[Dict[str, str]]]] = None
    work_experience: Optional[Union[str, List[Dict[str, str]]]] = None
    skills: Optional[Union[str, List[str]]] = None
    certifications: Optional[Union[str, List[str]]] = None
    projects: Optional[Union[str, List[Dict[str, str]]]] = None


@app.post("/generate-cv/")
async def generate_cv(user_input: UserQuery):
    input_data = {"raw_input": user_input.dict(exclude_none=True)}
    try:
        result = graph_executor.invoke(input_data)
        return {
            "message": result.get("message", "Success"),
            "latex": result.get("latex"),
        }
    except Exception as e:
        return {"error": str(e)}
