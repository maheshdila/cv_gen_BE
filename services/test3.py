import json
from workflows.cv_automation.crew import CVAutomationWorkflow

# Usage example
if __name__ == "__main__":
    # Example usage
    workflow = CVAutomationWorkflow()

    # Sample payload (replace with actual data)
    with open(r"D:\Projects\Professional Portfolio Project\cv_gen_BE\templates\payload_ramindu.json", 'r') as f:
        sample_payload = json.load(f)

    for k,v in sample_payload.items():
        print(f"{k}: {v}")

    try:
        final_result = workflow.run(sample_payload, "my-cv-bucket")
        print(f"Success! CV URL: {final_result['final_cv_url']}")
    except Exception as ex:
        print(f"Error: {ex}")