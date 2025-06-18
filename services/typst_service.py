import os
from datetime import datetime
import typst
from util.typst_util import TypstDocument
from models.user import FormData


# Generate the provided résumé
def generate_resume_typst(overview: str, form_data: FormData, output_filename: str):
    personal_details: dict = form_data.personalDetails

    # Initialize the document with personal information
    doc = TypstDocument(
        full_name=personal_details.get("fullName"),
        address=personal_details.get("address"),
        email=personal_details.get("email"),
        github=personal_details.get("gitHub"),
        linkedin=personal_details.get("linkedIn"),
        phone=personal_details.get("phone"),
        portfolio=personal_details.get("portfolio")
    )

    # Add sections
    doc.add_header_section()
    doc.add_overview_section(overview_content=overview)
    doc.add_education_section(education_list=form_data.education)
    doc.add_work_experience_section(work_experience_list=form_data.workExperience)
    doc.add_project_section(projects_list=form_data.projects)
    doc.add_skills_section(skills_list=form_data.skills)
    doc.add_achievements_section(achievements_list=form_data.achievements)
    doc.add_certifications_section(certifications_list=form_data.certifications)
    doc.add_references_section(references_list=form_data.referees)

    # Save Typst source to the file
    doc.save_to_file(output_filename)
    print(f"Typst resume generated successfully! Saved to {output_filename}")



# Compile a .typ file into a .pdf
def compile_typst_to_pdf(typst_filename: str, pdf_filename: str):
    typst.compile(
        input=typst_filename,
        output=pdf_filename
    )
    print(f"PDF resume generated successfully! Saved to {pdf_filename}")
    #return pdf_filename


# Entry point for generating and compiling from a JSON payload
def generate_resume(workflow_context:dict ,overview: str, form_data: FormData):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Get the absolute path to the project root
    project_root = os.path.dirname(os.path.abspath(__file__))  # services/
    project_root = os.path.abspath(os.path.join(project_root, ".."))  # move to project_root/

    # Absolute filepaths
    typst_output_filename = os.path.join(project_root, "cv", "typ", f"cv_{timestamp}.typ")
    pdf_output_filename = os.path.join(project_root, "cv", "pdf", f"cv_{timestamp}.pdf")
    workflow_context["cv_path"] =pdf_output_filename
    # Ensure directories exist
    os.makedirs(os.path.dirname(typst_output_filename), exist_ok=True)
    os.makedirs(os.path.dirname(pdf_output_filename), exist_ok=True)

    # Generate and compile
    generate_resume_typst(
        overview=overview,
        form_data=form_data,
        output_filename=typst_output_filename
    )
    compile_typst_to_pdf(typst_output_filename, pdf_output_filename)

    return pdf_output_filename
