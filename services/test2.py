import json
from services.typst_service import generate_resume


# Generate the résumé
if __name__ == "__main__":
    input_json_ramindu = r"D:\Projects\Professional Portfolio Project\cv_gen_BE\templates\payload_ramindu.json"
    input_json_omalya = r"D:\Projects\Professional Portfolio Project\cv_gen_BE\templates\payload_omalya.json"

    with open(input_json_omalya, 'r') as f:
        json_payload = json.load(f)

    for k,v in json_payload.items():
        print(f"{k}: {v}")

    generate_resume(overview="#lorem(100)", form_data=json_payload)
    print("Resume generated successfully!")