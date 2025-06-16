from pydantic import BaseModel
from typing import Optional, Dict, List, Union, Any

class FormData(BaseModel):
    personalDetails: Optional[Dict[str, Any]] = None
    education: Optional[List[Dict[str, Any]]] = None
    workExperience: Optional[List[Dict[str, Any]]] = None
    skills: Optional[List[Dict[str, Any]]] = None
    certifications: Optional[List[Dict[str, str]]] = None
    projects: Optional[List[Dict[str, Any]]] = None
    achievements : Optional[List[Dict[str, str]]] = None
    referees : Optional[List[Dict[str, str]]] = None


class UserQuery(BaseModel):
    jobDescription: Optional[str] = None
    formData: Optional[FormData] = None