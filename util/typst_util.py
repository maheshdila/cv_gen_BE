class TypstDocument:
    def __init__(self, full_name="", email="", phone="", address="",
                 linkedin="", github="", portfolio="", accent_color="#26428b",
                 font="New Computer Modern", paper="us-letter"):
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
        self.sections = []


    @staticmethod
    def _format_dates(start_date, end_date="Present"):
        """Helper function to format dates"""
        return f'dates-helper(start-date: "{start_date}", end-date: "{end_date}")'


    def add_header_section(self):
        """Generate the document header with personal info"""
        header = f"""#import "@preview/basic-resume:0.2.8": *
        
// Personal Information"
#let full-name = "{self.full_name}"
#let address = "{self.address}"
#let email = "{self.email}"
#let github = "{self.github}"
#let linkedin = "{self.linkedin}"
#let phone = "{self.phone}"
#let portfolio = "{self.portfolio}"

#show: resume.with(
  author: full-name,
  location: address,
  email: email,
  github: github,
  linkedin: linkedin,
  phone: phone,
  personal-site: portfolio,
  accent-color: "{self.accent_color}",
  font: "{self.font}",
  paper: "{self.paper}",
  author-position: center,
  personal-info-position: left,
)"""

        self.sections.append(header)


    def add_overview_section(self, overview_content: str):
        """Add overview section"""
        if not overview_content:
            raise Exception("Overview content cannot be empty")

        overview = f"== Overview\n\n{overview_content}"

        self.sections.append(overview)


    def add_education_section(self, education_list: list[dict]):
        """Add education section"""
        if not education_list:
            raise Exception("Education list cannot be empty")

        edu_content = "== Education"

        for component in education_list:
            edu_content += self.format_education_component(component)

        self.sections.append(edu_content)


    def format_education_component(self, component: dict):
        """Add education component"""
        content = f"""

#edu(
  institution: "{component.get("institution")}",
  location: "",
  dates: {self._format_dates(component.get("startDate"), "Present" if component.get("currentlyStudying") else component.get("endDate"))},
  degree: "{component.get("degree")} {f'({component.get("fieldOfStudy")})' if (component.get("fieldOfStudy") and component.get("fieldOfStudy")!="") else ""}"
)"""

        if component.get("description") and component.get("description")!="":
            content += f"\n  - {component.get("description")}"

        return content


    def add_work_experience_section(self, work_experience_list: list[dict]):
        """Add work experience section"""
        if not work_experience_list:
            raise Exception("Work experience list cannot be empty")

        work_content = "== Work Experience"

        for component in work_experience_list:
            work_content += self.format_work_experience_component(component)

        self.sections.append(work_content)


    def format_work_experience_component(self, component: dict):
        """Add work experience component"""
        content = f"""
        
#work(
  title: "{component.get("jobTitle")}",
  location: "{component.get("location")}",
  company: "{component.get("company")}",
  dates: {self._format_dates(component.get("startDate"), "Present" if component.get("currentlyWorking") else component.get("endDate"))},
)"""

        if component.get("description") and component.get("description")!="":
            content += f"\n  - {component.get("description")}"

        return content


    def add_project_section(self, projects_list: list[dict]):
        """Add project section"""
        if not projects_list:
            raise Exception("Projects list cannot be empty")

        project_content = "== Projects"

        for component in projects_list:
            project_content += self.format_project_component(component)

        self.sections.append(project_content)


    def format_project_component(self, component: dict):
        """Add a project component"""
        content = f"""
        
#project(
  name: "{component.get("name")}",
  dates: {self._format_dates(component.get("startDate"), "Present" if component.get("endDate")=="" else component.get("endDate"))},
  url: "{component.get("link")}"
)
  - {component.get("description")}
  - *Skills*: {', '.join(component.get("skills"))}"""

        return content


    def add_certifications_section(self, certifications_list: list[dict]):
        """Add a certificate section"""
        if not certifications_list:
            # raise Exception("Certifications list cannot be empty")
            return

        cert_content = "== Certifications"

        for component in certifications_list:
            cert_content += self.format_certification_component(component)

        self.sections.append(cert_content)


    @staticmethod
    def format_certification_component(component: dict):
        """Add certificate component"""
        content = f"""
        
#certificates(
  name: "{component.get("title")}",
  issuer: "{component.get("issuer")}",
  date: "{component.get("date")}",
  url: "{component.get("link")}"
)"""

        return content


    def add_skills_section(self, skills_list):
        """Add skills section"""
        if not skills_list:
            raise Exception("Skills list cannot be empty")

        skills_content = "== Skills"

        for component in skills_list:
            skills_content += self.format_skills_component(component)

        self.sections.append(skills_content)


    @staticmethod
    def format_skills_component(component: dict):
        """Add skills component"""
        content = f"""
- *{component.get("category")}*: {', '.join(component.get("technologies"))}"""

        return content


    def save_to_file(self, filename):
        """Generate the complete Typst document and save it to a file"""
        document = '\n\n'.join(self.sections)

        # Fix common encoding issues
        document = document.replace("â€™", "\'")
        document = document.replace("â€“", "-")

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(document)