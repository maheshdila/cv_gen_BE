from datetime import datetime
from typing import Any
import re

class TypstDocument:
    """Optimized TypstDocument class for generating resume templates"""

    def __init__(self, full_name: str = "", email: str = "", phone: str = "",
                 address: str = "", linkedin: str = "", github: str = "",
                 portfolio: str = "", accent_color: str = "#26428b",
                 font: str = "New Computer Modern", paper: str = "us-letter"):
        self.full_name = full_name
        self.email = email
        self.phone = phone
        self.address = address
        self.linkedin = linkedin
        self.github = github
        self.portfolio = portfolio
        self.accent_color = accent_color
        self.font = font
        self.paper = paper
        self.sections: list[str] = []


    def __len__(self) -> int:
        """Return number of sections"""
        return len(self.sections)


    def __str__(self) -> str:
        """String representation showing document info"""
        return f"TypstDocument(name='{self.full_name}', sections={len(self.sections)})"


    def clear_sections(self) -> None:
        """Clear all sections - useful for reusing the same instance"""
        self.sections.clear()


    @staticmethod
    def _format_dates(start_date: str, end_date: str = "Present") -> str:
        """Helper function to format dates with validation"""
        if not start_date:
            raise ValueError("Start date cannot be empty")

        # # Validate date format (basic check)
        # date_pattern = r'^[A-Za-z]{3}\s\d{4}$|^\d{4}$|^[A-Za-z]+\s\d{4}$'
        # if not re.match(date_pattern, start_date):
        #     raise ValueError(f"Invalid start date format: {start_date}")

        start_date = datetime.strptime(start_date, "%Y-%m").strftime("%b %Y")

        end_date = datetime.strptime(end_date, "%Y-%m").strftime("%b %Y") if end_date else "Present"

        return f'dates-helper(start-date: "{start_date}", end-date: "{end_date}")'


    @staticmethod
    def _escape_typst_string(text: str) -> str:
        """Escape special characters for Typst"""
        if not text:
            return ""

        # Common encoding fixes and Typst escaping
        replacements = {
            "â€™": "'",
            "â€“": "-"
        }

        for old, new in replacements.items():
            text = text.replace(old, new)

        return text


    @staticmethod
    def _validate_required_fields(data: dict[str, Any], required_fields: list[str], context: str) -> None:
        """Validate required fields in the data dictionary"""
        missing_fields = [field for field in required_fields if not data.get(field)]
        if missing_fields:
            raise ValueError(f"Missing required fields in {context}: {', '.join(missing_fields)}")


    def add_header_section(self) -> None:
        """Generate the document header with personal info"""
        # Validate required personal information
        if not self.full_name:
            raise ValueError("Full name is required")

        header = f"""#import "@preview/basic-resume:0.2.8": *

// Personal Information
#let full-name = "{self._escape_typst_string(self.full_name)}"

#show: resume.with(
  author: full-name,
  author-position: center,
  accent-color: "{self.accent_color}",
  font: "{self.font}",
  paper: "{self.paper}"
)

#grid(
  columns: (1fr, 1fr, 1fr),
  align(center)[
    phone: #link("tel:{self._escape_typst_string(self.phone)}") \\
    address: {self._escape_typst_string(self.address)}
  ],
  align(center)[
    #link("mailto:{self._escape_typst_string(self.email)}") \\
    #link("{self._escape_typst_string(self.portfolio)}") 
  ],
  align(center)[
    #link("{self._escape_typst_string(self.github)}")[GitHub] \\
    #link("{self._escape_typst_string(self.linkedin)}")[LinkedIn] 
  ]
)"""

        self.sections.append(header)


    def add_overview_section(self, overview_content: str) -> None:
        """Add an overview section with validation"""
        if not overview_content or not overview_content.strip():
            raise ValueError("Overview content cannot be empty")

        escaped_content = self._escape_typst_string(overview_content.strip())
        overview = f"== Overview\n\n{escaped_content}"
        self.sections.append(overview)


    def add_education_section(self, education_list: list[dict[str, Any]]) -> None:
        """Add an education section with improved validation"""
        if not education_list:
            raise ValueError("Education list cannot be empty")

        edu_content = "== Education"

        for i, component in enumerate(education_list):
            try:
                self._validate_required_fields(
                    component,
                    ["institution", "degree", "startDate"],
                    f"education item {i + 1}"
                )
                edu_content += self._format_education_component(component)
            except (ValueError, KeyError) as e:
                raise ValueError(f"Error in education item {i + 1}: {str(e)}")

        self.sections.append(edu_content)


    def _format_education_component(self, component: dict[str, Any]) -> str:
        """Format education component with better string handling"""
        institution = self._escape_typst_string(component["institution"])
        degree = self._escape_typst_string(component["degree"])
        field_of_study = component.get("fieldOfStudy", "")

        # Build degree string
        degree_text = degree
        if field_of_study and field_of_study.strip():
            degree_text += f" ({self._escape_typst_string(field_of_study)})"

        # Format dates
        end_date = None if component.get("currentlyStudying", False) else component.get("endDate")
        dates = self._format_dates(component["startDate"], end_date)

        content = f'''

#edu(
  institution: "{institution}",
  location: "",
  dates: {dates},
  degree: "{degree_text}"
)'''

        # Add description if present
        description = component.get("description", "")
        if description and description.strip():
            escaped_desc = self._escape_typst_string(description.strip())
            content += f"\n- {escaped_desc}"

        return content


    def add_work_experience_section(self, work_experience_list: list[dict[str, Any]]) -> None:
        """Add a work experience section with validation"""
        if not work_experience_list:
            raise ValueError("Work experience list cannot be empty")

        work_content = "== Work Experience"

        for i, component in enumerate(work_experience_list):
            try:
                self._validate_required_fields(
                    component,
                    ["jobTitle", "company", "startDate"],
                    f"work experience item {i + 1}"
                )
                work_content += self._format_work_experience_component(component)
            except (ValueError, KeyError) as e:
                raise ValueError(f"Error in work experience item {i + 1}: {str(e)}")

        self.sections.append(work_content)


    def _format_work_experience_component(self, component: dict[str, Any]) -> str:
        """Format work experience component"""
        job_title = self._escape_typst_string(component["jobTitle"])
        company = self._escape_typst_string(component["company"])
        location = self._escape_typst_string(component.get("location", ""))

        # Format dates
        end_date = None if component.get("currentlyWorking", False) else component.get("endDate")
        dates = self._format_dates(component["startDate"], end_date)

        content = f'''

#work(
  title: "{job_title}",
  location: "{location}",
  company: "{company}",
  dates: {dates},
)'''

        # Add description if present
        description = component.get("description", "")
        if description and description.strip():
            escaped_desc = self._escape_typst_string(description.strip())
            content += f"\n- {escaped_desc}"

        return content


    def add_project_section(self, projects_list: list[dict[str, Any]]) -> None:
        """Add a project section with validation"""
        if not projects_list:
            raise ValueError("Projects list cannot be empty")

        project_content = "== Projects"

        for i, component in enumerate(projects_list):
            try:
                self._validate_required_fields(
                    component,
                    ["name", "startDate"],
                    f"project item {i + 1}"
                )
                project_content += self._format_project_component(component)
            except (ValueError, KeyError) as e:
                raise ValueError(f"Error in project item {i + 1}: {str(e)}")

        self.sections.append(project_content)


    def _format_project_component(self, component: dict[str, Any]) -> str:
        """Format project component with better handling"""
        name = self._escape_typst_string(component["name"])
        link = self._escape_typst_string(component.get("link", ""))

        # Handle end date logic
        end_date = component.get("endDate", "")
        if not end_date or end_date.strip() == "":
            end_date = None

        dates = self._format_dates(component["startDate"], end_date)

        content = f"""

#link("{link}")[🔗]
#project(
  name: "{name}",
  dates: {dates}
)"""

        # Add description
        description = component.get("description", "")
        if description and description.strip():
            escaped_desc = self._escape_typst_string(description.strip())
            content += f"\n- {escaped_desc}"

        # Add skills
        skills = component.get("skills", [])
        if skills:
            skills_text = ", ".join(self._escape_typst_string(skill) for skill in skills if skill)
            if skills_text:
                content += f"\n  - *Skills*: {skills_text}"

        return content


    def add_certifications_section(self, certifications_list: list[dict[str, Any]]) -> None:
        """Add certifications section - now properly handles empty lists"""
        if not certifications_list:
            return  # Silently skip if no certifications

        cert_content = "== Certifications"

        for i, component in enumerate(certifications_list):
            try:
                self._validate_required_fields(
                    component,
                    ["title", "issuer"],
                    f"certification item {i + 1}"
                )
                cert_content += self._format_certification_component(component)
            except (ValueError, KeyError) as e:
                raise ValueError(f"Error in certification item {i + 1}: {str(e)}")

        self.sections.append(cert_content)


    def _format_certification_component(self, component: dict[str, Any]) -> str:
        """Format certification component"""
        title = self._escape_typst_string(component["title"])
        issuer = self._escape_typst_string(component["issuer"])
        date = self._escape_typst_string(component.get("date", ""))
        link = self._escape_typst_string(component.get("link", ""))

        content = f"""

#link("{link}")[🔗]
#certificates(
  name: "{title}",
  issuer: "{issuer}",
  date: "{date}"
)"""

        return content


    def add_achievements_section(self, achievements_list: list[dict[str, Any]]) -> None:
        """Add achievements section - now properly handles empty lists"""
        if not achievements_list:
            return  # Silently skip if no achievements

        achieve_content = "== Achievements"

        for i, component in enumerate(achievements_list):
            try:
                self._validate_required_fields(
                    component,
                    ["title"],
                    f"achievement item {i + 1}"
                )
                achieve_content += self._format_achievement_component(component)
            except (ValueError, KeyError) as e:
                raise ValueError(f"Error in achievement item {i + 1}: {str(e)}")

        self.sections.append(achieve_content)


    def _format_achievement_component(self, component: dict[str, Any]) -> str:
        """Format achievement component"""
        title = self._escape_typst_string(component["title"])
        date = self._escape_typst_string(component.get("date", ""))
        description = self._escape_typst_string(component.get("description", ""))

        content = f"""

#certificates(
  name: "{title}",
  date: "{date}"
)"""

        if description and description.strip():
            escaped_desc = self._escape_typst_string(description.strip())
            content += f"\n- {escaped_desc}"

        return content


    def add_skills_section(self, skills_list: list[dict[str, Any]]) -> None:
        """Add a skills section with validation"""
        if not skills_list:
            raise ValueError("Skills list cannot be empty")

        skills_content = "== Skills"

        for i, component in enumerate(skills_list):
            try:
                self._validate_required_fields(
                    component,
                    ["category", "technologies"],
                    f"skills item {i + 1}"
                )
                skills_content += self._format_skills_component(component)
            except (ValueError, KeyError) as e:
                raise ValueError(f"Error in skills item {i + 1}: {str(e)}")

        self.sections.append(skills_content)


    def _format_skills_component(self, component: dict[str, Any]) -> str:
        """Format skills component with better validation"""
        category = self._escape_typst_string(component["category"])
        technologies = component["technologies"]

        if not isinstance(technologies, list):
            raise ValueError("Technologies must be a list")

        # Filter out empty technologies and escape them
        tech_list = [self._escape_typst_string(tech) for tech in technologies if tech and tech.strip()]

        if not tech_list:
            raise ValueError("Technologies list cannot be empty")

        tech_string = ", ".join(tech_list)

        return f"\n- *{category}*: {tech_string}"


    def add_references_section(self, references_list: list[dict[str, Any]]) -> None:
        """Add references section - now properly handles empty lists"""
        if not references_list:
            return  # Silently skip if no references

        ref_content = f"""== References
        
#grid(
  columns: ({', '.join(['1fr' for _ in range(len(references_list))])}),
"""

        ref_lst: list[str] = []

        for i, component in enumerate(references_list):
            try:
                self._validate_required_fields(
                    component,
                    ["name", "position", "company", "email", "phone"],
                    f"reference item {i + 1}"
                )
                ref_lst.append(self._format_reference_component(component))
            except (ValueError, KeyError) as e:
                raise ValueError(f"Error in reference item {i + 1}: {str(e)}")

        ref_content += ',\n'.join(ref_lst) + '\n)'
        self.sections.append(ref_content)


    def _format_reference_component(self, component: dict[str, Any]) -> str:
        """Format reference component"""
        name = self._escape_typst_string(component["name"])
        position = self._escape_typst_string(component["position"])
        company = self._escape_typst_string(component["company"])
        email = self._escape_typst_string(component["email"])
        phone = self._escape_typst_string(component["phone"])

        content = f"""  align(left)[
    *{name}* \\
    _{position}_, \\
    _{company}_ \\
    email: #link("mailto:{email}") \\
    phone: #link("tel:{phone}") \\
  ]"""

        return content


    def generate_document(self) -> str:
        """Generate the complete Typst document as string"""
        if not self.sections:
            raise ValueError("No sections added to document")

        return '\n\n#linebreak()\n\n'.join(self.sections)


    def save_to_file(self, filename: str) -> None:
        """Generate and save the complete Typst document to a file"""
        if not filename:
            raise ValueError("Filename cannot be empty")

        if not filename.endswith('.typ'):
            filename += '.typ'

        document = self.generate_document()

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(document)
        except IOError as e:
            raise IOError(f"Failed to write file {filename}: {str(e)}")