"""
CV Automation Agents
Defines all specialized agents for the CV automation workflow
"""

from crewai import Agent, LLM
from langchain_community.llms import HuggingFaceHub
from tools import ContentAnalyzer, ContentReorderer, DateSorter, CVGenerator, ATSScorer


class CVAutomationAgents:
    """Factory class for creating specialized CV automation agents"""

    def __init__(self, llm: HuggingFaceHub):
        self.llm = llm
        self.content_analyzer = ContentAnalyzer()
        self.content_reorderer = ContentReorderer()
        self.date_sorter = DateSorter()
        self.cv_generator = CVGenerator()
        self.ats_scorer = ATSScorer()

    def create_resume_analyzer(self) -> Agent:
        """Creates an agent specialized in analyzing resumes and job requirements"""
        return Agent(
            role="Resume Data Analyst",
            goal="Analyze job descriptions and resume data to identify key requirements and matching opportunities",
            backstory="""You are an expert resume analyst with years of experience in talent acquisition 
            and HR. You excel at understanding job requirements and identifying how candidate profiles 
            can be best positioned to match those requirements. You have a keen eye for detail and 
            understand what recruiters and ATS systems look for in resumes.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=[self.content_analyzer]
        )

    def create_overview_writer(self) -> Agent:
        """Creates an agent specialized in writing compelling resume overviews"""
        return Agent(
            role="Professional Resume Writer",
            goal="Create compelling and tailored resume overview sections (100 words long) that highlight the candidate's best qualities for the specific job role",
            backstory="""You are a professional resume writer with expertise in crafting compelling 
            personal statements and overview sections. You know how to distill a candidate's experience 
            and skills into a powerful narrative that captures attention and demonstrates value. You 
            understand the psychology of hiring managers and how to make candidates stand out.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )

    def create_content_optimizer(self) -> Agent:
        """Creates an agent specialized in optimizing content relevance"""
        return Agent(
            role="Content Optimization Specialist",
            goal="Reorder and optimize resume sections (projects, skills, certifications, achievements) to best match job requirements",
            backstory="""You are a content strategist who specializes in resume optimization. You have 
            a deep understanding of how to prioritize and arrange information to maximize impact. You 
            know that the order of information can make or break a resume's effectiveness, and you're 
            skilled at identifying which experiences and skills are most relevant for specific roles.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=[self.content_reorderer]
        )

    def create_chronology_organizer(self) -> Agent:
        """Creates an agent specialized in organizing chronological information"""
        return Agent(
            role="Chronological Data Organizer",
            goal="Organize education and work experience in proper reverse chronological order (most recent first)",
            backstory="""You are a meticulous data organizer with expertise in chronological arrangement 
            of professional and educational history. You understand the importance of presenting career 
            progression in a clear, logical manner that tells a coherent story. You're detail-oriented 
            and ensure that dates are properly formatted and sequenced.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=[self.date_sorter]
        )

    def create_pdf_generator(self) -> Agent:
        """Creates an agent specialized in PDF generation and formatting"""
        return Agent(
            role="Document Generation Specialist",
            goal="Generate professional PDF resumes using the Typst service with optimized formatting and layout",
            backstory="""You are a document formatting expert who specializes in creating visually 
            appealing and professional documents. You understand the importance of clean, readable 
            formatting and know how to present information in a way that's both attractive and 
            ATS-friendly. You're skilled with various document generation tools and ensure high-quality output.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=[self.cv_generator]
        )

    def create_quality_assessor(self) -> Agent:
        """Creates an agent specialized in quality assessment and ATS scoring"""
        return Agent(
            role="Quality Assurance & ATS Specialist",
            goal="Assess resume quality, calculate ATS scores, and provide optimization recommendations",
            backstory="""You are a quality assurance expert who specializes in ATS (Applicant Tracking 
            System) optimization. You have deep knowledge of how ATS systems parse and score resumes, 
            and you understand what makes a resume both human-readable and machine-friendly. You're 
            analytical and provide actionable feedback for improvement.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=[self.ats_scorer]
        )

    def create_optimization_strategist(self) -> Agent:
        """Creates an agent specialized in iterative optimization strategy"""
        return Agent(
            role="Optimization Strategy Expert",
            goal="Analyze ATS feedback and develop strategies for improving resume performance in subsequent iterations",
            backstory="""You are a strategic optimization expert who excels at analyzing performance 
            data and developing improvement strategies. You understand how to interpret ATS scores and 
            feedback to make targeted improvements. You're systematic in your approach and focus on 
            high-impact changes that will significantly boost resume performance.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )