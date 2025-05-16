# === langgraph_cv_pipeline.py ===

from langgraph.graph import StateGraph, END

# from langgraph.checkpoint import MemorySaver
from pydantic import BaseModel
from typing import Dict, Any
import google.generativeai as genai
from jinja2 import Environment, FileSystemLoader
import subprocess
import json
import re

# === Configure Gemini ===
API_KEY = "AIzaSyB9jeDjHFp319jUiiBNaibr4KPrn9ylpDY"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-2.0-pro")

# === LaTeX setup ===
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


# === Utility ===
def clean_json_string(model_output: str) -> str:
    cleaned_output = re.sub(
        r"```json\\s*|\\s*```", "", model_output.strip(), flags=re.MULTILINE
    )
    cleaned_output = cleaned_output.replace("'", '"')
    return cleaned_output


# === LangGraph Agent: ExtractStructuredData ===
def extract_structured_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    input_json = json.dumps(state.raw_input, indent=2)
    prompt = f"""
    Extract the following fields from this user input:
    - name, email, phone, linkedin, github, summary
    - education (list with degree, university, years, gpa, coursework)
    - work_experience (list with job_title, company, location, years, bullet_points)
    - skills (list)
    - certifications (list)
    - projects (list with name, link, description)
    Input:
    ```json
    {input_json}
    ```
    Output JSON only.
    """
    response = model.generate_content(prompt)
    cleaned = clean_json_string(response.text)
    structured_data = json.loads(cleaned)
    return {"structured_data": structured_data}


# === LangGraph Agent: ATS Optimization ===
def ats_optimization_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    data = state["structured_data"]
    prompt = f"""
    Optimize this resume data for ATS compliance.
    - Convert summaries into strong, keyword-rich statements
    - Convert job experience into action-verb bullet points
    - Avoid images/graphics and follow standard formatting
    - Keep it quantifiable and industry-specific
    Input:
    ```json
    {json.dumps(data, indent=2)}
    ```
    Output structured JSON only.
    """
    response = model.generate_content(prompt)
    optimized = clean_json_string(response.text)
    return {"optimized_data": json.loads(optimized)}


# === LangGraph Agent: Render LaTeX ===
def render_cv_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    rendered_cv = latex_template.render(**state["optimized_data"])
    with open("output/cv.tex", "w", encoding="utf-8") as f:
        f.write(rendered_cv)
    subprocess.run(["pdflatex", "cv.tex"], cwd="output", check=True)
    return {"message": "CV rendered and compiled", "latex": rendered_cv}


class CVState(BaseModel):
    raw_input: dict
    extracted_data: dict = None
    ats_optimized_data: dict = None
    latex_code: str = None


# === Build LangGraph ===
workflow = StateGraph(state_schema=CVState)
workflow.add_node("extract", extract_structured_agent)
workflow.add_node("ats_optimize", ats_optimization_agent)
workflow.add_node("render", render_cv_agent)
workflow.set_entry_point("extract")
workflow.add_edge("extract", "ats_optimize")
workflow.add_edge("ats_optimize", "render")
workflow.add_edge("render", END)

graph_executor = workflow.compile()

initial_input = {
    "raw_input": {
        "name": "John Smith",
        "github": "https://github.com/johnsmith",
        "education": [
            {"degree": "BSc", "institution": "ABC University", "year": "2020"}
        ],
        "skills": ["Python", "FastAPI"],
        "projects": [{"title": "Cool App", "description": "Did stuff"}],
    }
}

result = graph_executor.invoke(initial_input)


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
    input_data = {"user_input": user_input.dict(exclude_none=True)}
    try:
        result = graph_executor.invoke(input_data)
        return {
            "message": result.get("message", "Success"),
            "latex": result.get("latex"),
        }
    except Exception as e:
        return {"error": str(e)}
