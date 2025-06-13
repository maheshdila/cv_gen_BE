from pydantic import BaseModel
from typing import Optional, Dict, List, Union

class UserQuery(BaseModel):
    name: Optional[str] = None
    other_bio_data: Optional[Dict[str, str]] = None
    summary: Optional[str] = None
    education: Optional[Union[str, List[Dict[str, str]]]] = None
    work_experience: Optional[Union[str, List[Dict[str, str]]]] = None
    skills: Optional[Union[str, List[str]]] = None
    certifications: Optional[Union[str, List[str]]] = None
    projects: Optional[Union[str, List[Dict[str, str]]]] = None
