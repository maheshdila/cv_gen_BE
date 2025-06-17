"""
CV Automation Tasks
Defines all tasks for the CV automation workflow
"""

from crewai import Task, Agent


class CVAutomationTasks:
    """Factory class for creating CV automation tasks"""

    @staticmethod
    def create_analyze_payload_task(agent: Agent) -> Task:
        """Task for analyzing the payload and job requirements"""
        return Task(
            description="""
            Analyze the provided payload containing job description and candidate data.

            Your tasks:
            1. Extract key requirements from the job description including:
               - Required skills and technologies
               - Experience level and years
               - Industry domain knowledge
               - Soft skills and competencies

            2. Analyze the candidate's profile from formData:
               - Current skills and experience
               - Educational background
               - Project experience
               - Achievements and certifications

            3. Identify matching strengths and potential gaps
            4. Create a relevance ranking for candidate's experiences

            Context: {payload}
            Current iteration: {iteration}

            Expected Output: A comprehensive analysis report with:
            - Job requirements breakdown
            - Candidate profile summary
            - Match score and gaps analysis
            - Recommendations for highlighting key strengths
            """,
            agent=agent,
            expected_output="Detailed analysis report in JSON format with job requirements, candidate strengths, and optimization recommendations"
        )

    @staticmethod
    def create_generate_overview_task(agent: Agent, job_description: str, form_data: dict) -> Task:
        """Task for generating a compelling resume overview"""
        return Task(
            description="""
            Create a compelling resume overview/summary paragraph that perfectly aligns with the job requirements.

            Your tasks:
            1. Use the analysis from the previous task to understand key requirements
            2. Craft a 3-4 sentence overview that:
               - Highlights the candidate's most relevant experience
               - Mentions key skills that match the job requirements
               - Demonstrates value proposition
               - Uses action words and quantifiable achievements when possible

            3. Ensure the overview is:
               - Tailored specifically to this job description
               - Professional and engaging
               - Not sorter than 100 words
               - Using first person perspective
               - Not using any names of the projects or certifications
               - Discussing the skills in projects
               - ATS-friendly with relevant keywords
               - Concise but impactful

            Context: {form_data}
            Job Description: {job_description}
            Analysis Report: Available from previous task

            Expected Output: A professional overview paragraph (3-4 sentences) that will serve as the resume summary
            """,
            agent=agent,
            expected_output="A compelling 3-4 sentence resume overview paragraph optimized for the specific job requirements"
        )

    @staticmethod
    def create_optimize_content_task(agent: Agent) -> Task:
        """Task for optimizing content relevance order"""
        return Task(
            description="""
            Reorder the projects, skills, certifications, and achievements arrays to best match the job requirements.

            Your tasks:
            1. For each array (projects, skills, certifications, achievements):
               - Analyze relevance to the job description
               - Score each item based on alignment with requirements
               - Reorder with most relevant items first

            2. Specific reordering criteria:
               - Projects: Prioritize by technology stack match, domain relevance, and complexity
               - Skills: Group by category and prioritize based on job requirements
               - Certifications: Prioritize industry-relevant and recent certifications
               - Achievements: Prioritize quantifiable results and relevant accomplishments

            3. Maintain original data structure while reordering
            4. Ensure no data is lost or modified, only reordered

            Context: {optimized_payload}
            Job Requirements: Available from analysis task

            Expected Output: Updated payload with all arrays reordered for maximum job relevance
            """,
            agent=agent,
            expected_output="Updated payload object with reordered arrays (projects, skills, certifications, achievements) optimized for job relevance"
        )

    @staticmethod
    def create_organize_chronology_task(agent: Agent, job_description: str, form_data: dict) -> Task:
        """Task for organizing chronological information"""
        return Task(
            description="""
            Organize education and work experience in proper reverse chronological order (most recent first), which matches the candidate's job description.

            Your tasks:
            1. Sort workExperience array:
               - Most recent positions first
               - Handle currentlyWorking flag (these go first)
               - Use startDate and endDate for sorting
               - Maintain all original data

            2. Sort education array:
               - Most recent education first
               - Handle currentlyStudying flag (these go first)
               - Use startDate and endDate for sorting
               - Maintain all original data

            3. Date handling:
               - Parse various date formats correctly
               - Handle incomplete dates appropriately
               - Ensure proper chronological ordering

            Context: {form_data}
            Job Description: {job_description}

            Expected Output: Updated payload with workExperience and education arrays sorted in reverse chronological order
            """,
            agent=agent,
            expected_output="Updated payload object with workExperience and education arrays sorted in reverse chronological order (most recent first)"
        )

    @staticmethod
    def create_generate_pdf_task(agent: Agent) -> Task:
        """Task for generating PDF using Typst service"""
        return Task(
            description="""
            Generate a professional CV PDF using the Typst service.

            Your tasks:
            1. Prepare the data for Typst service:
               - Use the generated overview from the overview task
               - Use the optimized and chronologically ordered payload
               - Ensure all data is properly formatted

            2. Call TypstService.generate_cv(overview, optimized_payload):
               - Pass the overview string as first parameter
               - Pass the fully optimized payload as second parameter
               - Handle any errors gracefully

            3. Verify PDF generation:
               - Check that the PDF file was created successfully
               - Verify file exists in the cv/ directory
               - Ensure file is not empty or corrupted

            Context: 
            - Overview: {overview}
            - Optimized Payload: {optimized_payload}

            Expected Output: Path to the generated CV PDF file
            """,
            agent=agent,
            expected_output="File path to the successfully generated CV PDF in the cv/ directory"
        )

    @staticmethod
    def create_assess_quality_task(agent: Agent) -> Task:
        """Task for assessing CV quality and ATS score"""
        return Task(
            description="""
            Assess the generated CV's quality and calculate ATS score.

            Your tasks:
            1. Extract text content from the generated PDF
            2. Calculate ATS score based on:
               - Keyword matching with job description
               - Skills alignment
               - Experience relevance
               - Education match
               - Overall content quality

            3. Provide detailed feedback:
               - Current ATS score (0-100)
               - Strengths identified
               - Areas for improvement
               - Specific recommendations for optimization

            4. If score < 85, provide specific optimization suggestions:
               - Keywords to add or emphasize
               - Content sections to improve
               - Skills to highlight more prominently

            Context:
            - CV Path: {cv_path}
            - Job Description: {jobDescription}
            - Current Iteration: {iteration}
            - Target Score: {target_ats_score}

            Expected Output: ATS assessment report with score and optimization recommendations
            """,
            agent=agent,
            expected_output="ATS assessment report with numerical score (0-100) and detailed feedback for optimization"
        )

    @staticmethod
    def create_optimization_strategy_task(agent: Agent) -> Task:
        """Task for developing optimization strategy for next iteration"""
        return Task(
            description="""
            Analyze the ATS assessment and develop an optimization strategy for the next iteration.

            Your tasks:
            1. Review the ATS assessment results
            2. Identify the top 3 areas for improvement
            3. Develop specific optimization strategies:
               - Content modifications
               - Keyword enhancements
               - Section reordering
               - Skills emphasis changes

            4. Create an updated payload with optimizations:
               - Enhance descriptions with relevant keywords
               - Adjust skill categories and emphasis
               - Optimize project descriptions
               - Refine achievements and certifications

            5. Prepare overview optimization suggestions

            Context:
            - ATS Score: {current_ats_score}
            - Assessment Report: Available from previous task
            - Current Payload: {optimized_payload}
            - Iteration: {iteration}

            Expected Output: Optimization strategy with updated payload and overview suggestions
            """,
            agent=agent,
            expected_output="Optimization strategy document with updated payload and specific improvement recommendations"
        )