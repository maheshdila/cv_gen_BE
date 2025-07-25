"""
CV Automation Workflow - Main Orchestrator
Handles the complete CV generation and optimization process using Crew AI
"""
import json
import os
from dotenv import load_dotenv
from typing import Any
from datetime import datetime

from crewai import Crew, Process, LLM

from models.user import UserQuery
from .agents import CVAutomationAgents
from .tasks import CVAutomationTasks
from .tools import ATSScorer, S3Uploader
from .utils import PayloadValidator

from services.typst_service import generate_resume
from services.s3Uploader import upload_to_s3_agent

class CVAutomationWorkflow:
    """Main workflow orchestrator for CV automation using Crew AI"""

    def __init__(self):
        self.llm = self._setup_llm()
        self.agents = CVAutomationAgents(self.llm)
        self.tasks = CVAutomationTasks()
        self.ats_scorer = ATSScorer()
        self.s3_uploader = S3Uploader()
        self.payload_validator = PayloadValidator()


    @staticmethod
    def _setup_llm() -> LLM:
        """Setup Gemini LLM"""
        token_label = "GEMINI_API_KEY"
        load_dotenv()
        token = os.getenv(token_label)

        if not token:
            raise ValueError(f"{token_label} not found in environment variables")

        os.environ[token_label] = token

        return LLM(
            model="gemini/gemini-2.0-flash",
            temperature=0.7,
        )


    def run(self, payload: UserQuery, s3_bucket_name: str) -> dict[str, Any]:
        """
        Main workflow execution

        Args:
            payload: Input data containing job description and form data
            s3_bucket_name: S3 bucket name for final CV upload

        Returns:
            Dict containing final CV URL and processing details
        """
        # print(payload)
        try:
            # Validate payload
            self.payload_validator.validate(payload)

            print("Starting CV Automation Workflow...")

            # Initialize workflow context
            workflow_context = {
                "job_description": payload.jobDescription,
                "form_data": dict(payload.formData),
                "s3_bucket_name": s3_bucket_name,
                "iteration": 0,
                "max_iterations": 1,
                "target_ats_score": 85,
                "current_ats_score": 0,
                "optimized_form_data": dict(payload.formData),
                "overview": "",
                "cv_path": "",
                "final_cv_url": ""
            }

            # Run the optimization loop
            # while (workflow_context["iteration"] < workflow_context["max_iterations"] and
            #        workflow_context["current_ats_score"] < workflow_context["target_ats_score"]):
            for i in range(1):
                workflow_context["iteration"] += 1
                print(f"\nIteration {workflow_context['iteration']}/{workflow_context['max_iterations']}")

                # Create and run the crew for this iteration
                crew = self._create_crew(workflow_context)
                result = crew.kickoff(inputs=workflow_context)

                # Update context with results
                workflow_context.update(result)

                print(f"Result: {result}")

                workflow_context['overview'] = str(result)

                # print(f"Overview: {workflow_context['overview']}")

                # print(f"ATS Score: {workflow_context['current_ats_score']}/100")

                if workflow_context["current_ats_score"] >= workflow_context["target_ats_score"]:
                    print("Target ATS score achieved!")
                    break
                elif workflow_context["iteration"] < workflow_context["max_iterations"]:
                    print("Optimizing for next iteration...")

            print("Generating CV from optimized form data...")
            pdf_path=generate_resume(workflow_context,workflow_context["overview"], payload.formData)
            print("pdf path from crew is ",pdf_path)
            print("pdf path from workflow{cv path}",workflow_context["cv_path"])

            workflow_context["final_cv_url"] = upload_to_s3_agent(workflow_context["cv_path"])



            #Upload final CV to S3
            #if workflow_context["cv_path"]:


            #     final_url = self.s3_uploader.upload_cv(
            #         workflow_context["cv_path"],
            #         s3_bucket_name
            #     )
            #     workflow_context["final_cv_url"] = final_url
            #     print(f"CV uploaded to S3: {final_url}")
            # else:
            #     raise Exception("No CV file generated")

            # return {
            #     "success": True,
            #     "final_cv_url": workflow_context["final_cv_url"],
            #     "ats_score": workflow_context["current_ats_score"],
            #     "iterations_used": workflow_context["iteration"],
            #     "processing_time": datetime.now().isoformat()
            # }

            return {
                "success": True,
                "pdf path": workflow_context["cv_path"],
                "cv_url": workflow_context["final_cv_url"]
            }

        except Exception as e:
            print(f"Workflow failed: {str(e)}")
            raise Exception(f"CV Automation Workflow failed: {str(e)}")


    def _create_crew(self, context: dict[str, Any]) -> Crew:
        """Create Crew AI crew for a single iteration"""

        # Get all agents
        # resume_analyzer = self.agents.create_resume_analyzer()
        overview_writer = self.agents.create_overview_writer()
        # content_optimizer = self.agents.create_content_optimizer()
        # chronology_organizer = self.agents.create_chronology_organizer()
        # pdf_generator = self.agents.create_pdf_generator()
        # quality_assessor = self.agents.create_quality_assessor()

        # Create tasks for this iteration
        tasks = [
            # self.tasks.create_analyze_payload_task(resume_analyzer),
            self.tasks.create_generate_overview_task(agent=overview_writer, job_description=context.get("job_description"), form_data=context.get("form_data")),
            # self.tasks.create_optimize_content_task(content_optimizer),
            # self.tasks.create_organize_chronology_task(chronology_organizer),
            # self.tasks.create_generate_pdf_task(pdf_generator),
            # self.tasks.create_assess_quality_task(quality_assessor)
        ]

        # Create crew
        crew = Crew(
            name=f"CV Automation Crew - Iteration {context['iteration']}",
            agents=[
                # resume_analyzer,
                overview_writer,
                # content_optimizer,
                # chronology_organizer,
                # pdf_generator,
                # quality_assessor
            ],
            tasks=tasks,
            process=Process.sequential,
            verbose=True
        )

        return crew