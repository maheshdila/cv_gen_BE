# === langgraph_cv_pipeline.py ===

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



# === Gemini API Key and Setup ===
API_KEY = "AIzaSyB9jeDjHFp319jUiiBNaibr4KPrn9ylpDY"  # Replace with your actual API key
genai.configure(api_key=API_KEY)

# === Choose the Gemini Model ===
model = genai.GenerativeModel("gemini-2.0-flash")

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
        r"```json\s*|```", "", model_output.strip(), flags=re.MULTILINE
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

    # Remove triple backticks and optional "json"
    cleaned = re.sub(
        r"^```(?:json)?\s*|\s*```$", "", cleaned.strip(), flags=re.IGNORECASE
    )

    if not cleaned.strip():
        raise ValueError("Cleaned response is empty after stripping markdown.")

    try:
        structured_data = json.loads(cleaned)
        return {"extracted_data": structured_data}
    except json.JSONDecodeError as e:
        raise ValueError(
            f"Failed to decode JSON from cleaned response:\n{cleaned}"
        ) from e


# === LangGraph Agent: ATS Optimization ===
def ats_optimization_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    data = state.extracted_data
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

    optimized = re.sub(
        r"^```(?:json)?\s*|\s*```$", "", optimized.strip(), flags=re.IGNORECASE
    )

    if not optimized.strip():
        raise ValueError("Optimized response is empty.")

    try:
        return {"ats_optimized_data": json.loads(optimized)}
    except json.JSONDecodeError as e:
        raise ValueError(
            f"Failed to decode JSON from optimized response:\n{optimized}"
        ) from e


# === LangGraph Agent: Render LaTeX ===
# def render_cv_agent(state: Dict[str, Any]) -> Dict[str, Any]:
#     rendered_cv = latex_template.render(**state.ats_optimized_data)
#     with open("output/cv.tex", "w", encoding="utf-8") as f:
#         f.write(rendered_cv)
#     subprocess.run(["pdflatex", "cv.tex"], cwd="output", check=True)
#     return {"message": "CV rendered and compiled", "latex": rendered_cv}


def render_cv_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    # Extract email if present
    email = state.ats_optimized_data.get("email", "anonymous")

    # Hash email and timestamp
    #safe_email_hash = hashlib.sha256(email.encode()).hexdigest()[:10]
    safe_email_hash = "demo"
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    output_dir = f"output/cv_{safe_email_hash}_{timestamp}"
    os.makedirs(output_dir, exist_ok=True)

    # Render LaTeX
    rendered_cv = latex_template.render(**state.ats_optimized_data)

    # Write .tex file
    tex_path = os.path.join(output_dir, "cv.tex")
    with open(tex_path, "w", encoding="utf-8") as f:
        f.write(rendered_cv)

    # Simulate `yes | pdflatex cv.tex`
    # process = subprocess.run(
    #     ["pdflatex", "cv.tex"],
    #     cwd=output_dir,
    #     input=b"y\n" * 10,  # simulate multiple 'y' inputs
    #     stdout=subprocess.PIPE,
    #     stderr=subprocess.PIPE,
    #     check=True
    # )
    subprocess.run(
        "yes | pdflatex cv.tex",
        cwd=output_dir,
        shell=True,
        check=True
    )

    pdf_path = os.path.join(output_dir, "cv.pdf")

    return {
        "message": "CV rendered and compiled",
        "latex": rendered_cv,
        "pdf_path": pdf_path,
        "directory": output_dir
    }

# === LangGraph Agent: Upload to S3 ===
class NoCredentialsError:
    pass


# === LangGraph Agent: Upload to S3 ===
def upload_to_s3_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    pdf_path = state["pdf_path"]
    email = state["ats_optimized_data"].get("email", "anonymous")
    safe_email_hash = "demo"
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    s3_key = f"cvs/{safe_email_hash}_{timestamp}.pdf"
    bucket_name = "cv-bucket-protfolio-app"  # Replace with your actual bucket name
    region_name = "ap-southeast-1"  # Replace with your AWS region (e.g., "us-east-1")

    s3_client = boto3.client("s3", region_name=region_name)

    try:
        s3_client.upload_file(pdf_path, bucket_name, s3_key)
        print(f"File uploaded to s3://{bucket_name}/{s3_key} in region {region_name}")

        # Generate pre-signed URL
        presigned_url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket_name, 'Key': s3_key},
            ExpiresIn=3600
        )
        return {"s3_url": presigned_url}
    except FileNotFoundError:
        return {"error": f"Error: PDF file not found at {pdf_path}"}
    except NoCredentialsError:
        return {"error": "Error: AWS credentials not found. Make sure IAM role is attached."}
    except Exception as e:
        return {"error": f"Error uploading to S3: {str(e)}"}





# === LangGraph Setup ===
class CVState(BaseModel):
    raw_input: dict
    extracted_data: dict = None
    ats_optimized_data: dict = None
    latex_code: str = None
    pdf_path: str = None
    directory: str = None
    s3_url:str = None


workflow = StateGraph(state_schema=CVState)
workflow.add_node("extract", extract_structured_agent)
workflow.add_node("ats_optimize", ats_optimization_agent)
workflow.add_node("render", render_cv_agent)
workflow.add_node("upload",upload_to_s3_agent)
workflow.set_entry_point("extract")
workflow.add_edge("extract", "ats_optimize")
workflow.add_edge("ats_optimize", "render")
workflow.add_edge("render", "upload")
workflow.add_edge("upload",END)


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
            "pdf_path":result.get("pdf_path"),
            "s3_url": result.get("s3_url")
        }
    except Exception as e:
        return {"error": str(e)}





@app.get("/test")
def api_test():
    return {"fast api server is up and running..."}
