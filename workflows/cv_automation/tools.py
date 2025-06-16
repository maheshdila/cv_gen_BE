"""
CV Automation Tools
Custom tools for the CV automation workflow
"""

import os
import json
import boto3
import PyPDF2
from datetime import datetime
from typing import Any
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
import re
from collections import Counter
import math


class ContentAnalyzer(BaseTool):
    """Tool for analyzing job descriptions and candidate profiles"""

    name: str = "Content Analyzer"
    description: str = "Analyzes job descriptions and candidate data to identify key requirements and matches"

    def _run(self, job_description: str, candidate_data: dict[str, Any]) -> dict[str, Any]:
        """Analyze content and return structured insights"""
        try:
            # Extract job requirements
            job_requirements = self._extract_job_requirements(job_description)

            # Analyze candidate profile
            candidate_profile = self._analyze_candidate_profile(candidate_data)

            # Calculate match scores
            match_analysis = self._calculate_matches(job_requirements, candidate_profile)

            return {
                "job_requirements": job_requirements,
                "candidate_profile": candidate_profile,
                "match_analysis": match_analysis,
                "recommendations": self._generate_recommendations(match_analysis)
            }
        except Exception as e:
            raise Exception(f"Content analysis failed: {str(e)}")

    def _extract_job_requirements(self, job_description: str) -> dict[str, Any]:
        """Extract key requirements from the job description"""
        # Common tech skills patterns
        tech_keywords = [
            'python', 'java', 'javascript', 'react', 'nodejs', 'aws', 'docker',
            'kubernetes', 'sql', 'mongodb', 'postgresql', 'git', 'jenkins',
            'terraform', 'ansible', 'linux', 'windows', 'azure', 'gcp'
        ]

        # Extract mentioned technologies
        found_tech = []
        for tech in tech_keywords:
            if tech.lower() in job_description.lower():
                found_tech.append(tech)

        # Extract experience requirements
        experience_match = re.search(r'(\d+)[\+\-\s]*years?\s+(?:of\s+)?experience', job_description.lower())
        required_experience = int(experience_match.group(1)) if experience_match else 0

        return {
            "required_technologies": found_tech,
            "required_experience_years": required_experience,
            "job_level": self._determine_job_level(job_description),
            "industry_keywords": self._extract_industry_keywords(job_description)
        }

    def _analyze_candidate_profile(self, candidate_data: dict[str, Any]) -> dict[str, Any]:
        """Analyze candidate's profile and experience"""
        skills = []
        for skill_cat in candidate_data.get('skills', []):
            skills.extend(skill_cat.get('technologies', []))

        # Calculate total experience
        total_experience = self._calculate_total_experience(candidate_data.get('workExperience', []))

        return {
            "skills": skills,
            "total_experience_years": total_experience,
            "project_count": len(candidate_data.get('projects', [])),
            "education_level": self._determine_education_level(candidate_data.get('education', [])),
            "certifications_count": len(candidate_data.get('certifications', []))
        }

    @staticmethod
    def _calculate_matches(job_req: dict, candidate: dict) -> dict[str, Any]:
        """Calculate match scores between job and candidate"""
        # Technology match
        job_tech = set(tech.lower() for tech in job_req.get('required_technologies', []))
        candidate_tech = set(skill.lower() for skill in candidate.get('skills', []))
        tech_match = len(job_tech.intersection(candidate_tech)) / max(len(job_tech), 1) * 100

        # Experience match
        req_exp = job_req.get('required_experience_years', 0)
        candidate_exp = candidate.get('total_experience_years', 0)
        exp_match = min(candidate_exp / max(req_exp, 1), 1.0) * 100

        return {
            "technology_match": tech_match,
            "experience_match": exp_match,
            "overall_match": (tech_match + exp_match) / 2
        }

    @staticmethod
    def _generate_recommendations(match_analysis: dict) -> list[str]:
        """Generate optimization recommendations"""
        recommendations = []

        if match_analysis["technology_match"] < 70:
            recommendations.append("Emphasize relevant technologies in project descriptions")

        if match_analysis["experience_match"] < 70:
            recommendations.append("Highlight years of experience in overview and work history")

        recommendations.append("Use keywords from job description throughout the resume")

        return recommendations

    @staticmethod
    def _determine_job_level(job_description: str) -> str:
        """Determine job level from description"""
        if any(word in job_description.lower() for word in ['senior', 'lead', 'principal']):
            return 'senior'
        elif any(word in job_description.lower() for word in ['junior', 'entry', 'graduate']):
            return 'junior'
        return 'mid'

    @staticmethod
    def _extract_industry_keywords(job_description: str) -> list[str]:
        """Extract industry-specific keywords"""
        # This is a simplified implementation
        common_keywords = ['agile', 'scrum', 'devops', 'ci/cd', 'microservices', 'api', 'rest', 'graphql']
        found_keywords = []
        for keyword in common_keywords:
            if keyword.lower() in job_description.lower():
                found_keywords.append(keyword)
        return found_keywords

    @staticmethod
    def _calculate_total_experience(work_experience: list[dict]) -> float:
        """Calculate total years of experience"""
        total_months = 0
        for job in work_experience:
            start_date = job.get('startDate', '')
            end_date = job.get('endDate', '') if not job.get('currentlyWorking', False) else datetime.now().strftime('%Y-%m')

            if start_date and end_date:
                try:
                    start = datetime.strptime(start_date, '%Y-%m')
                    end = datetime.strptime(end_date, '%Y-%m')
                    months = (end.year - start.year) * 12 + (end.month - start.month)
                    total_months += months
                except:
                    # Fallback: assume 2 years per job if date parsing fails
                    total_months += 24

        return round(total_months / 12, 1)

    @staticmethod
    def _determine_education_level(education: list[dict]) -> str:
        """Determine the highest education level"""
        if not education:
            return 'none'

        degrees = [edu.get('degree', '').lower() for edu in education]

        if any('phd' in degree or 'doctorate' in degree for degree in degrees):
            return 'doctorate'
        elif any('master' in degree or 'msc' in degree or 'mba' in degree for degree in degrees):
            return 'masters'
        elif any('bachelor' in degree or 'bsc' in degree or 'ba' in degree for degree in degrees):
            return 'bachelors'
        else:
            return 'other'


class ContentReorderer(BaseTool):
    """Tool for reordering content based on job relevance"""

    name: str = "Content Reorderer"
    description: str = "Reorders projects, skills, certifications, and achievements based on job relevance"

    def _run(self, payload: dict[str, Any], job_requirements: dict[str, Any]) -> dict[str, Any]:
        """Reorder content arrays based on relevance"""
        try:
            optimized_payload = payload.copy()
            form_data = optimized_payload['formData']

            # Reorder projects
            if 'projects' in form_data:
                form_data['projects'] = self._reorder_projects(
                    form_data['projects'],
                    job_requirements
                )

            # Reorder skills
            if 'skills' in form_data:
                form_data['skills'] = self._reorder_skills(
                    form_data['skills'],
                    job_requirements
                )

            # Reorder certifications
            if 'certifications' in form_data:
                form_data['certifications'] = self._reorder_certifications(
                    form_data['certifications'],
                    job_requirements
                )

            # Reorder achievements
            if 'achievements' in form_data:
                form_data['achievements'] = self._reorder_achievements(
                    form_data['achievements'],
                    job_requirements
                )

            return optimized_payload

        except Exception as e:
            raise Exception(f"Content reordering failed: {str(e)}")

    @staticmethod
    def _reorder_projects(projects: list[dict], job_req: dict) -> list[dict]:
        """Reorder projects based on relevance to job requirements"""
        def project_relevance_score(project):
            score = 0
            project_skills = project.get('skills', [])
            required_tech = job_req.get('required_technologies', [])

            # Technology match
            for skill in project_skills:
                if skill.lower() in [tech.lower() for tech in required_tech]:
                    score += 10

            # Recent projects get higher scores
            if project.get('currentlyWorking', False):
                score += 5

            # Projects with links/demos get bonus
            if project.get('link', ''):
                score += 3

            return score

        return sorted(projects, key=project_relevance_score, reverse=True)

    @staticmethod
    def _reorder_skills(skills: list[dict], job_req: dict) -> list[dict]:
        """Reorder skills based on job requirements"""
        def skill_category_relevance(skill_cat):
            score = 0
            technologies = skill_cat.get('technologies', [])
            required_tech = job_req.get('required_technologies', [])

            # Count matching technologies
            for tech in technologies:
                if tech.lower() in [req_tech.lower() for req_tech in required_tech]:
                    score += 10

            # Prioritize programming languages and frameworks
            category = skill_cat.get('category', '').lower()
            if any(keyword in category for keyword in ['programming', 'framework', 'language']):
                score += 5

            return score

        return sorted(skills, key=skill_category_relevance, reverse=True)

    @staticmethod
    def _reorder_certifications(certifications: list[dict], job_req: dict) -> list[dict]:
        """Reorder certifications based on relevance and recency"""
        def certification_relevance(cert):
            score = 0
            title = cert.get('title', '').lower()
            required_tech = job_req.get('required_technologies', [])

            # Check if certification matches required technologies
            for tech in required_tech:
                if tech.lower() in title:
                    score += 15

            # Recent certifications get higher scores
            cert_date = cert.get('date', '')
            if cert_date:
                try:
                    cert_year = int(cert_date.split('-')[0])
                    current_year = datetime.now().year
                    if current_year - cert_year <= 2:
                        score += 10
                    elif current_year - cert_year <= 5:
                        score += 5
                except:
                    pass

            # Certifications with links get a bonus
            if cert.get('link', ''):
                score += 3

            return score

        return sorted(certifications, key=certification_relevance, reverse=True)

    @staticmethod
    def _reorder_achievements(achievements: list[dict], job_req: dict) -> list[dict]:
        """Reorder achievements based on relevance and impact"""
        def achievement_relevance(achievement):
            score = 0
            description = achievement.get('description', '').lower()
            title = achievement.get('title', '').lower()
            required_tech = job_req.get('required_technologies', [])

            # Check for technology mentions
            for tech in required_tech:
                if tech.lower() in description or tech.lower() in title:
                    score += 10

            # Look for quantifiable results
            if re.search(r'\d+%|\$\d+|\d+x|increase|improve|reduce|save', description):
                score += 8

            # Recent achievements get higher scores
            ach_date = achievement.get('date', '')
            if ach_date:
                try:
                    ach_year = int(ach_date.split('-')[0])
                    current_year = datetime.now().year
                    if current_year - ach_year <= 2:
                        score += 5
                except:
                    pass

            return score

        return sorted(achievements, key=achievement_relevance, reverse=True)


class DateSorter(BaseTool):
    """Tool for sorting chronological data"""

    name: str = "Date Sorter"
    description: str = "Sorts work experience and education in reverse chronological order"

    def _run(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Sort chronological data"""
        try:
            sorted_payload = payload.copy()
            form_data = sorted_payload['formData']

            # Sort work experience
            if 'workExperience' in form_data:
                form_data['workExperience'] = self._sort_work_experience(
                    form_data['workExperience']
                )

            # Sort education
            if 'education' in form_data:
                form_data['education'] = self._sort_education(
                    form_data['education']
                )

            return sorted_payload

        except Exception as e:
            raise Exception(f"Date sorting failed: {str(e)}")

    @staticmethod
    def _sort_work_experience(work_exp: list[dict]) -> list[dict]:
        """Sort work experience in reverse chronological order"""
        def work_sort_key(job):
            # Currently working jobs go first
            if job.get('currentlyWorking', False):
                return (1, datetime.now())

            # Parse end date
            end_date = job.get('endDate', '')
            if end_date:
                try:
                    return (0, datetime.strptime(end_date, '%Y-%m'))
                except:
                    try:
                        return (0, datetime.strptime(end_date, '%Y'))
                    except:
                        return (0, datetime.min)

            # Fallback to start date
            start_date = job.get('startDate', '')
            if start_date:
                try:
                    return (0, datetime.strptime(start_date, '%Y-%m'))
                except:
                    try:
                        return (0, datetime.strptime(start_date, '%Y'))
                    except:
                        return (0, datetime.min)

            return (0, datetime.min)

        return sorted(work_exp, key=work_sort_key, reverse=True)

    @staticmethod
    def _sort_education(education: list[dict]) -> list[dict]:
        """Sort education in reverse chronological order"""
        def education_sort_key(edu):
            # Currently studying goes first
            if edu.get('currentlyStudying', False):
                return (1, datetime.now())

            # Parse end date
            end_date = edu.get('endDate', '')
            if end_date:
                try:
                    return (0, datetime.strptime(end_date, '%Y-%m'))
                except:
                    try:
                        return (0, datetime.strptime(end_date, '%Y'))
                    except:
                        return (0, datetime.min)

            # Fallback to start date
            start_date = edu.get('startDate', '')
            if start_date:
                try:
                    return (0, datetime.strptime(start_date, '%Y-%m'))
                except:
                    try:
                        return (0, datetime.strptime(start_date, '%Y'))
                    except:
                        return (0, datetime.min)

            return (0, datetime.min)

        return sorted(education, key=education_sort_key, reverse=True)


class CVGenerator(BaseTool):
    """Tool for generating CV using Typst service"""

    name: str = "CV Generator"
    description: str = "Generates CV PDF using the Typst service"

    @staticmethod
    def _run(overview: str, payload: dict[str, Any]) -> str:
        """Generate CV using Typst service"""
        try:
            # Import the Typst service (assuming it's available in the project)
            from typst_service import TypstService

            # Generate CV
            cv_path = TypstService.generate_cv(overview, payload)

            # Verify the file was created
            if not os.path.exists(cv_path):
                raise Exception(f"CV file was not created at {cv_path}")

            # Check if a file is not empty
            if os.path.getsize(cv_path) == 0:
                raise Exception("Generated CV file is empty")

            return cv_path

        except ImportError:
            raise Exception("TypstService not found. Make sure it's properly imported.")
        except Exception as e:
            raise Exception(f"CV generation failed: {str(e)}")


class ATSScorer(BaseTool):
    """Tool for calculating ATS scores"""

    name: str = "ATS Scorer"
    description: str = "Calculates ATS scores for generated CVs"

    def _run(self, cv_path: str, job_description: str) -> dict[str, Any]:
        """Calculate ATS score for the CV"""
        try:
            # Extract text from PDF
            cv_text = self._extract_pdf_text(cv_path)

            # Calculate various scoring metrics
            keyword_score = self._calculate_keyword_score(cv_text, job_description)
            format_score = self._calculate_format_score(cv_text)
            content_score = self._calculate_content_score(cv_text)

            # Calculate overall ATS score
            overall_score = (keyword_score * 0.5 + format_score * 0.3 + content_score * 0.2)

            return {
                "overall_score": round(overall_score, 2),
                "keyword_score": round(keyword_score, 2),
                "format_score": round(format_score, 2),
                "content_score": round(content_score, 2),
                "feedback": self._generate_feedback(overall_score, keyword_score, format_score, content_score),
                "recommendations": self._generate_recommendations(overall_score, cv_text, job_description)
            }

        except Exception as e:
            raise Exception(f"ATS scoring failed: {str(e)}")

    @staticmethod
    def _extract_pdf_text(pdf_path: str) -> str:
        """Extract text from a PDF file"""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text()
                return text
        except Exception as e:
            raise Exception(f"Failed to extract text from PDF: {str(e)}")

    def _calculate_keyword_score(self, cv_text: str, job_description: str) -> float:
        """Calculate the keyword matching score"""
        # Extract keywords from job description
        job_keywords = self._extract_keywords(job_description)
        cv_keywords = self._extract_keywords(cv_text)

        if not job_keywords:
            return 50.0  # Default score if no keywords found

        # Calculate match percentage
        matched_keywords = set(job_keywords).intersection(set(cv_keywords))
        match_percentage = len(matched_keywords) / len(job_keywords) * 100

        return min(match_percentage, 100.0)

    @staticmethod
    def _calculate_format_score(cv_text: str) -> float:
        """Calculate format and structure score"""
        score = 0

        # Check for common sections
        sections = ['experience', 'education', 'skills', 'projects']
        for section in sections:
            if section.lower() in cv_text.lower():
                score += 15

        # Check for contact information
        if re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', cv_text):
            score += 10

        # Check for phone number
        if re.search(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', cv_text):
            score += 10

        # Check for dates
        if re.search(r'\b\d{4}\b', cv_text):
            score += 10

        return min(score, 100.0)

    @staticmethod
    def _calculate_content_score(cv_text: str) -> float:
        """Calculate content quality score"""
        score = 0

        # Check for quantifiable achievements
        if re.search(r'\d+%|\$\d+|\d+x|increase|improve|reduce|save', cv_text.lower()):
            score += 30

        # Check for action verbs
        action_verbs = ['developed', 'implemented', 'designed', 'created', 'managed', 'led', 'improved']
        for verb in action_verbs:
            if verb.lower() in cv_text.lower():
                score += 5

        # Check for adequate length
        word_count = len(cv_text.split())
        if word_count > 200:
            score += 20

        return min(score, 100.0)

    @staticmethod
    def _extract_keywords(text: str) -> list[str]:
        """Extract relevant keywords from text"""
        # Common technical keywords
        tech_keywords = [
            'python', 'java', 'javascript', 'react', 'nodejs', 'aws', 'docker',
            'kubernetes', 'sql', 'mongodb', 'postgresql', 'git', 'jenkins',
            'terraform', 'ansible', 'linux', 'windows', 'azure', 'gcp',
            'agile', 'scrum', 'devops', 'ci/cd', 'microservices', 'api'
        ]

        found_keywords = []
        text_lower = text.lower()

        for keyword in tech_keywords:
            if keyword in text_lower:
                found_keywords.append(keyword)

        return found_keywords

    @staticmethod
    def _generate_feedback(overall: float, keyword: float, format_score: float, content: float) -> str:
        """Generate feedback based on scores"""
        if overall >= 85:
            return "Excellent! Your CV meets ATS requirements."
        elif overall >= 70:
            return "Good CV, but could use some improvements for better ATS compatibility."
        else:
            return "CV needs significant improvements to pass ATS screening."

    def _generate_recommendations(self, score: float, cv_text: str, job_desc: str) -> list[str]:
        """Generate specific recommendations for improvement"""
        recommendations = []

        if score < 85:
            # Keyword recommendations
            job_keywords = self._extract_keywords(job_desc)
            cv_keywords = self._extract_keywords(cv_text)
            missing_keywords = set(job_keywords) - set(cv_keywords)

            if missing_keywords:
                recommendations.append(f"Add these keywords: {', '.join(list(missing_keywords)[:5])}")

            # Content recommendations
            if not re.search(r'\d+%|\$\d+|\d+x', cv_text):
                recommendations.append("Add quantifiable achievements with numbers and percentages")

            # Format recommendations
            if 'skills' not in cv_text.lower():
                recommendations.append("Add a dedicated skills section")

            if not re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', cv_text):
                recommendations.append("Ensure contact information is clearly visible")

        return recommendations


class S3Uploader(BaseTool):
    """Tool for uploading files to S3"""

    name: str = "S3 Uploader"
    description: str = "Uploads CV files to S3 bucket"

    @staticmethod
    def _run(file_path: str, bucket_name: str) -> str:
        """Upload the file to S3 and return URL"""
        try:
            # Initialize S3 client
            s3_client = boto3.client(
                's3',
                aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
                region_name=os.getenv('AWS_REGION', 'us-east-1')
            )

            # Generate unique filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"cv_{timestamp}.pdf"

            # Upload the file
            s3_client.upload_file(file_path, bucket_name, filename)

            # Generate URL
            url = f"https://{bucket_name}.s3.amazonaws.com/{filename}"

            return url

        except Exception as e:
            raise Exception(f"S3 upload failed: {str(e)}")

    def upload_cv(self, cv_path: str, bucket_name: str) -> str:
        """Public method for uploading CV"""
        return self._run(cv_path, bucket_name)