"""
CV Automation Utilities
Helper functions and validators for the CV automation workflow
"""

import json
import os
from typing import Dict, Any, List, Optional
from datetime import datetime
import re

from models.user import UserQuery, FormData


class PayloadValidator:
    """Validates payload structure and content"""

    def validate(self, payload: UserQuery) -> bool:
        """Validate payload structure and content"""
        try:
            # Check top-level structure
            if not isinstance(payload, UserQuery):
                raise ValueError("Payload must be a UserQuery object")

            # Check required fields
            required_fields = ['jobDescription', 'formData']
            for field in required_fields:
                if not hasattr(payload, field):
                    raise ValueError(f"Missing required field: {field}")

            # Validate job description
            if not isinstance(payload.jobDescription, str) or not payload.jobDescription.strip():
                raise ValueError("jobDescription must be a non-empty string")

            # Validate form data structure
            self._validate_form_data(payload.formData)

            return True

        except Exception as e:
            raise ValueError(f"Payload validation failed: {str(e)}")

    def _validate_form_data(self, form_data: FormData) -> bool:
        """Validate form data structure"""
        if not isinstance(form_data, FormData):
            raise ValueError("formData must be a FormData object")

        # Validate personal details
        if hasattr(form_data, 'personalDetails'):
            self._validate_personal_details(form_data.personalDetails)

        # Validate arrays
        array_fields = ['workExperience', 'education', 'projects', 'skills', 'achievements', 'certifications',
                        'referees']
        for field in array_fields:
            if hasattr(form_data, field):
                if not isinstance(getattr(form_data, field), list):
                    raise ValueError(f"{field} must be a list")

                # Validate array items based on type
                if field == 'workExperience':
                    self._validate_work_experience(form_data.workExperience)
                elif field == 'education':
                    self._validate_education(form_data.education)
                elif field == 'projects':
                    self._validate_projects(form_data.projects)
                elif field == 'skills':
                    self._validate_skills(form_data.skills)
                elif field == 'achievements':
                    self._validate_achievements(form_data.achievements)
                elif field == 'certifications':
                    self._validate_certifications(form_data.certifications)
                elif field == 'referees':
                    self._validate_referees(form_data.referees)

        return True

    @staticmethod
    def _validate_personal_details(personal_details: Dict[str, Any]) -> bool:
        """Validate personal details structure"""
        if not isinstance(personal_details, dict):
            raise ValueError("personalDetails must be a dictionary")

        # Check for essential fields
        essential_fields = ['fullName', 'email']
        for field in essential_fields:
            if field not in personal_details or not personal_details[field]:
                raise ValueError(f"Missing essential personal detail: {field}")

        # Validate email format
        email = personal_details.get('email', '')
        if email and not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            raise ValueError("Invalid email format")

        return True

    @staticmethod
    def _validate_work_experience(work_exp: List[Dict]) -> bool:
        """Validate work experience entries"""
        for job in work_exp:
            if not isinstance(job, dict):
                raise ValueError("Work experience entry must be a dictionary")

            required_fields = ['jobTitle', 'company']
            for field in required_fields:
                if field not in job or not job[field]:
                    raise ValueError(f"Missing required work experience field: {field}")

        return True

    @staticmethod
    def _validate_education(education: List[Dict]) -> bool:
        """Validate education entries"""
        for edu in education:
            if not isinstance(edu, dict):
                raise ValueError("Education entry must be a dictionary")

            required_fields = ['degree', 'institution']
            for field in required_fields:
                if field not in edu or not edu[field]:
                    raise ValueError(f"Missing required education field: {field}")

        return True

    @staticmethod
    def _validate_projects(projects: List[Dict]) -> bool:
        """Validate project entries"""
        for project in projects:
            if not isinstance(project, dict):
                raise ValueError("Project entry must be a dictionary")

            if 'name' not in project or not project['name']:
                raise ValueError("Project must have a name")

            if 'skills' in project and not isinstance(project['skills'], list):
                raise ValueError("Project skills must be a list")

        return True

    @staticmethod
    def _validate_skills(skills: List[Dict]) -> bool:
        """Validate skills entries"""
        for skill in skills:
            if not isinstance(skill, dict):
                raise ValueError("Skill entry must be a dictionary")

            if 'category' not in skill or not skill['category']:
                raise ValueError("Skill must have a category")

            if 'technologies' in skill and not isinstance(skill['technologies'], list):
                raise ValueError("Skill technologies must be a list")

        return True

    @staticmethod
    def _validate_achievements(achievements: List[Dict]) -> bool:
        """Validate achievement entries"""
        for achievement in achievements:
            if not isinstance(achievement, dict):
                raise ValueError("Achievement entry must be a dictionary")

            if 'title' not in achievement or not achievement['title']:
                raise ValueError("Achievement must have a title")

        return True

    @staticmethod
    def _validate_certifications(certifications: List[Dict]) -> bool:
        """Validate certification entries"""
        for cert in certifications:
            if not isinstance(cert, dict):
                raise ValueError("Certification entry must be a dictionary")

            required_fields = ['title', 'issuer']
            for field in required_fields:
                if field not in cert or not cert[field]:
                    raise ValueError(f"Missing required certification field: {field}")

        return True

    @staticmethod
    def _validate_referees(referees: List[Dict]) -> bool:
        """Validate referee entries"""
        for referee in referees:
            if not isinstance(referee, dict):
                raise ValueError("Referee entry must be a dictionary")

            required_fields = ['name', 'position']
            for field in required_fields:
                if field not in referee or not referee[field]:
                    raise ValueError(f"Missing required referee field: {field}")

        return True


class ConfigManager:
    """Manages configuration and environment variables"""

    @staticmethod
    def get_env_var(var_name: str, default: Optional[str] = None) -> str:
        """Get environment variable with optional default"""
        value = os.getenv(var_name, default)
        if value is None:
            raise ValueError(f"Environment variable {var_name} not found")
        return value

    @staticmethod
    def validate_required_env_vars() -> bool:
        """Validate that all required environment variables are set"""
        required_vars = [
            'HUGGINGFACE_API_KEY',
            'AWS_ACCESS_KEY_ID',
            'AWS_SECRET_ACCESS_KEY'
        ]

        missing_vars = []
        for var in required_vars:
            if not os.getenv(var):
                missing_vars.append(var)

        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

        return True


class FileManager:
    """Manages file operations for the workflow"""

    @staticmethod
    def ensure_directory_exists(directory_path: str) -> bool:
        """Ensure a directory exists, create if it doesn't"""
        try:
            os.makedirs(directory_path, exist_ok=True)
            return True
        except Exception as e:
            raise Exception(f"Failed to create directory {directory_path}: {str(e)}")

    @staticmethod
    def clean_old_files(directory_path: str, max_age_hours: int = 24) -> bool:
        """Clean old files from the directory"""
        try:
            if not os.path.exists(directory_path):
                return True

            current_time = datetime.now()

            for filename in os.listdir(directory_path):
                file_path = os.path.join(directory_path, filename)
                if os.path.isfile(file_path):
                    file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                    age_hours = (current_time - file_time).total_seconds() / 3600

                    if age_hours > max_age_hours:
                        os.remove(file_path)
                        print(f"Removed old file: {filename}")

            return True
        except Exception as e:
            print(f"Warning: Failed to clean old files: {str(e)}")
            return False

    @staticmethod
    def save_payload_backup(payload: Dict[str, Any], workflow_id: str) -> str:
        """Save payload backup for debugging"""
        try:
            backup_dir = "workflows/cv_automation/backups"
            FileManager.ensure_directory_exists(backup_dir)

            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"payload_backup_{workflow_id}_{timestamp}.json"
            file_path = os.path.join(backup_dir, filename)

            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(payload, f, indent=2, ensure_ascii=False)

            return file_path
        except Exception as e:
            print(f"Warning: Failed to save payload backup: {str(e)}")
            return ""


class LogManager:
    """Manages logging for the workflow"""

    def __init__(self, workflow_id: str):
        self.workflow_id = workflow_id
        self.logs = []

    def log(self, level: str, message: str, extra_data: Optional[Dict] = None):
        """Add log entry"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'workflow_id': self.workflow_id,
            'level': level,
            'message': message,
            'extra_data': extra_data or {}
        }

        self.logs.append(log_entry)

        # Print to console
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{timestamp}] [{level}] {message}")

    def info(self, message: str, extra_data: Optional[Dict] = None):
        """Log info message"""
        self.log('INFO', message, extra_data)

    def warning(self, message: str, extra_data: Optional[Dict] = None):
        """Log warning message"""
        self.log('WARNING', message, extra_data)

    def error(self, message: str, extra_data: Optional[Dict] = None):
        """Log error message"""
        self.log('ERROR', message, extra_data)

    def save_logs(self) -> str:
        """Save logs to file"""
        try:
            log_dir = "workflows/cv_automation/logs"
            FileManager.ensure_directory_exists(log_dir)

            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"workflow_log_{self.workflow_id}_{timestamp}.json"
            file_path = os.path.join(log_dir, filename)

            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.logs, f, indent=2, ensure_ascii=False)

            return file_path
        except Exception as e:
            print(f"Warning: Failed to save logs: {str(e)}")
            return ""


class MetricsCollector:
    """Collects and tracks workflow metrics"""

    def __init__(self):
        self.metrics = {
            'start_time': None,
            'end_time': None,
            'total_duration': 0,
            'iterations_used': 0,
            'final_ats_score': 0,
            'initial_ats_score': 0,
            'improvement_score': 0,
            'errors_encountered': 0,
            'tasks_completed': 0
        }

    def start_workflow(self):
        """Mark workflow start"""
        self.metrics['start_time'] = datetime.now()

    def end_workflow(self):
        """Mark workflow end and calculate duration"""
        self.metrics['end_time'] = datetime.now()
        if self.metrics['start_time']:
            duration = self.metrics['end_time'] - self.metrics['start_time']
            self.metrics['total_duration'] = duration.total_seconds()

    def record_iteration(self, iteration: int, ats_score: float):
        """Record iteration metrics"""
        self.metrics['iterations_used'] = iteration
        self.metrics['final_ats_score'] = ats_score

        if iteration == 1:
            self.metrics['initial_ats_score'] = ats_score

        self.metrics['improvement_score'] = (
                self.metrics['final_ats_score'] - self.metrics['initial_ats_score']
        )

    def record_error(self):
        """Record error occurrence"""
        self.metrics['errors_encountered'] += 1

    # def record_task_completion(self):