import json
from util.typst_util import TypstDocument


# Example usage to recreate the provided resume
def create_resume(payload, output_filename):
    personal_details: dict = payload.get("personalDetails")

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

    # Add the header
    doc.add_header_section()

    # Add overview
    doc.add_overview_section(overview_content="""Enthusiastic Data Science and Engineering student with practical experience in AI and ML fields, specializing in Python and TensorFlow. Skilled in building and optimizing machine learning algorithms for real-world applications, with a focus on data analysis and management. Eager to contribute to ML model development for real-world applications and leverage hands-on experience.""")

    # Add education
    doc.add_education_section(education_list=payload.get("education"))

    # Add work experiences
    doc.add_work_experience_section(work_experience_list=payload.get("workExperience"))

    # Add project
    doc.add_project_section(projects_list=payload.get("projects"))

    # Add skills
    doc.add_skills_section(skills_list=payload.get("skills"))

    # Add certifications
    doc.add_certifications_section(certifications_list=payload.get("certifications"))

    doc.save_to_file(output_filename)


# Generate the resume
if __name__ == "__main__":
    input_json_ramindu = r"D:\Projects\Professional Portfolio Project\cv_gen_BE\templates\payload_ramindu.json"
    input_json_omalya = r"D:\Projects\Professional Portfolio Project\cv_gen_BE\templates\payload_omalya.json"
    output_typst_ramindu = r"D:\Projects\Professional Portfolio Project\cv_gen_BE\templates\typst_ramindu.typ"
    output_typst_omalya = r"D:\Projects\Professional Portfolio Project\cv_gen_BE\templates\typst_omalya.typ"

    with open(input_json_ramindu, 'r') as f:
        json_payload = json.load(f)

    for k,v in json_payload.items():
        print(f"{k}: {v}")

    create_resume(json_payload, output_typst_ramindu)
    print("Resume generated successfully!")