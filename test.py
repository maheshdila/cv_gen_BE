import json
import google.generativeai as genai

# === CONFIG ===
API_KEY = "AIzaSyB9jeDjHFp319jUiiBNaibr4KPrn9ylpDY"  # <-- Replace this with your actual key
JSON_FILE = "cv_data\\cvData1.json"  # <-- Your file with one JSON record

# === SETUP ===
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

# === HELPER FUNCTION TO BUILD PROMPT ===
def build_prompt(data):
    bio = data.get("biography", "")
    experience = data.get("experience", [])
    projects = data.get("projects", [])
    role = data.get("desired_role", "Software Engineer")

    prompt = (
        "You are a professional resume writer. The user has shared the following details:\n\n"
        f"Bio: {bio}\n\n"
        f"Work Experience: {json.dumps(experience, indent=2)}\n\n"
        f"Projects: {json.dumps(projects, indent=2)}\n\n"
        f"The user wants to apply for the role of {role}.\n\n"
        "Generate a tailored, ATS-friendly CV for this role."
    )
    return prompt

# === LOAD JSON AND BUILD PROMPT ===
with open(JSON_FILE, "r") as f:
    record = json.load(f)

prompt = build_prompt(record)

# === CALL GEMINI API ===
response = model.generate_content(prompt)
print("\n===== GENERATED CV =====\n")
print(response.text)
