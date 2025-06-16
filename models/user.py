from pydantic import BaseModel
from typing import Optional, Dict, List, Union

class FormData(BaseModel):
    personalDetails: Optional[Dict[str, str]] = None
    education: Optional[Union[str, List[Dict[str, str]]]] = None
    workExperience: Optional[Union[str, List[Dict[str, str]]]] = None
    skills: Optional[Union[str, List[str]]] = None
    certifications: Optional[Union[str, List[str]]] = None
    projects: Optional[Union[str, List[Dict[str, str]]]] = None
    achievements : Optional[Union[str, List[str]]] = None
    referees : Optional[Union[str, List[str]]] = None


class UserQuery(BaseModel):
    jobDescription: Optional[str] = None
    formData: Optional[FormData] = None