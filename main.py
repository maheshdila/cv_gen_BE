from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Any, List
from pylatex import Document, Section, Subsection, Command, Itemize
from pylatex.utils import NoEscape
import pandas as pd
import os
import uuid

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


# === Core Generation Logic ===
def generate_cv_files(cv_data: dict, output_dir="output"):
    os.makedirs(output_dir, exist_ok=True)
    uid = str(uuid.uuid4())[:8]
    pdf_filename = os.path.join(output_dir, f"{uid}_cv.pdf")
    csv_filename = os.path.join(output_dir, f"{uid}_cv.csv")

    # === Generate PDF ===
    doc = Document(os.path.join(output_dir, f"{uid}_temp"))
    doc.preamble.append(Command("title", "Curriculum Vitae"))
    doc.preamble.append(Command("author", cv_data["contact"].get("email", "")))
    doc.append(NoEscape(r"\maketitle"))

    with doc.create(Section("Biography")):
        doc.append(cv_data["biography"])

    with doc.create(Section("Education")):
        for edu in cv_data["education"]:
            doc.append(f"{edu['degree']} from {edu['institution']} ({edu['year']})\n")

    with doc.create(Section("Experience")):
        for job in cv_data["experience"]:
            with doc.create(Subsection(job["title"])):
                doc.append(
                    f"{job['company']} | {job['duration']}\n\n{job['description']}"
                )

    with doc.create(Section("Projects")):
        for project in cv_data["projects"]:
            with doc.create(Subsection(project["name"])):
                doc.append(
                    f"Technologies: {', '.join(project['tech_stack'])}\n\n{project['description']}"
                )

    with doc.create(Section("Skills")):
        with doc.create(Itemize()) as itemize:
            for skill in cv_data["skills"]:
                itemize.add_item(skill)

    with doc.create(Section("Achievements")):
        with doc.create(Itemize()) as itemize:
            for ach in cv_data["achievements"]:
                itemize.add_item(ach)

    with doc.create(Section("Contact")):
        for key, value in cv_data["contact"].items():
            doc.append(f"{key.capitalize()}: {value}\n")

    doc.generate_pdf(os.path.splitext(pdf_filename)[0], clean_tex=True)

    # === Generate CSV ===
    rows = []
    for edu in cv_data["education"]:
        rows.append({"type": "education", **edu})
    for exp in cv_data["experience"]:
        rows.append({"type": "experience", **exp})
    for proj in cv_data["projects"]:
        proj_data = {
            "name": proj["name"],
            "tech_stack": ", ".join(proj["tech_stack"]),
            "description": proj["description"],
        }
        rows.append({"type": "project", **proj_data})
    for skill in cv_data["skills"]:
        rows.append({"type": "skill", "value": skill})
    for ach in cv_data["achievements"]:
        rows.append({"type": "achievement", "value": ach})

    df = pd.DataFrame(rows)
    df.to_csv(csv_filename, index=False)

    return pdf_filename, csv_filename


# === API Endpoint ===
@app.post("/generate-cv")
async def generate_cv(cv_data: CVData):
    try:
        pdf_path, csv_path = generate_cv_files(cv_data.dict())
        return {"pdf_path": pdf_path, "csv_path": csv_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
