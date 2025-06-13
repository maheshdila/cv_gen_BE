from pydantic import BaseModel
class CVState(BaseModel):
    raw_input: dict
    extracted_data: dict = None
    ats_optimized_data: dict = None
    latex_code: str = None
    pdf_path: str = None
    directory: str = None
    s3_url:str = None