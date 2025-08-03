import logging
import json
import os
from typing import Dict, Any, Optional
from langchain.tools import Tool
from pydantic import BaseModel, Field
import pypdf

logger = logging.getLogger(__name__)


class ResumeInfoInput(BaseModel):
    """Input schema for the resume info tool."""

    query: str = Field(
        description="Not used - the tool returns complete resume JSON regardless of input. Kept for compatibility."
    )


class ResumeInfo:
    """A tool for querying structured information from Peter's resume."""

    def __init__(self):
        self.resume_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "resources",
            "resume.pdf",
        )
        self.cache_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "resources",
            "resume_parsed.json",
        )
        self.resume_data = None
        self._initialize_resume_data()

    def _extract_pdf_text(self) -> str:
        """Extract text from the resume PDF."""
        try:
            with open(self.resume_path, "rb") as file:
                pdf_reader = pypdf.PdfReader(file)
                text_parts = []
                for page in pdf_reader.pages:
                    text_parts.append(page.extract_text())
                return "\n".join(text_parts)
        except Exception as e:
            logger.error(f"Error extracting PDF text: {str(e)}")
            raise

    def _parse_resume_with_claude(self, resume_text: str) -> Dict[str, Any]:
        """Use Claude to parse resume text into structured JSON."""
        try:
            # Import ChatAnthropic only when needed for parsing
            from langchain_anthropic import ChatAnthropic
            from langchain.schema import HumanMessage, SystemMessage

            # Initialize Claude
            llm = ChatAnthropic(
                model="claude-sonnet-4-20250514",
                temperature=0,
                max_tokens=4096,
            )

            # Create the parsing prompt
            system_prompt = """You are a resume parser. Extract information from the resume text and return it as valid JSON matching this exact schema:

{
  "personalInfo": {
    "name": "string",
    "title": "string",
    "summary": "string",
    "contact": {
      "email": "string",
      "phone": "string",
      "website": "string",
      "github": "string",
      "linkedin": "string"
    }
  },
  "technicalSkills": {
    "subjectExpertise": ["array of strings"],
    "programmingLanguages": ["array of strings"],
    "frameworks": ["array of strings"],
    "technologies": ["array of strings"],
    "paradigms": ["array of strings"]
  },
  "professionalExperience": [
    {
      "title": "string",
      "company": "string",
      "duration": "string",
      "description": "string (optional)",
      "responsibilities": ["array of strings"]
    }
  ],
  "education": [
    {
      "degree": "string",
      "field": "string",
      "institution": "string",
      "location": "string",
      "graduationYear": number
    }
  ],
  "publications": [
    {
      "authors": ["array of strings"],
      "title": "string",
      "journal": "string (optional)",
      "conference": "string (optional)",
      "volume": "string (optional)",
      "issue": "string (optional)",
      "pages": "string (optional)"
    }
  ]
}

Return ONLY valid JSON, no markdown formatting, no code blocks, no additional text or explanations. The response should start with { and end with }."""

            user_prompt = (
                f"Parse this resume into the specified JSON format:\n\n{resume_text}"
            )

            # Make the API call
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt),
            ]
            response = llm.invoke(messages)

            # Parse the JSON response
            response_text = response.content

            # Strip common markdown formatting if present
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            response_text = response_text.strip()

            parsed_data = json.loads(response_text)
            return parsed_data

        except json.JSONDecodeError as e:
            logger.error(f"Error parsing Claude's response as JSON: {str(e)}")
            logger.error(f"Raw response: {response.content[:500]}...")
            # Save full response for debugging
            debug_path = os.path.join(
                os.path.dirname(self.cache_path), "resume_parse_debug.txt"
            )
            with open(debug_path, "w") as f:
                f.write(response_text)
            logger.error(f"Full response saved to: {debug_path}")
            raise
        except Exception as e:
            logger.error(f"Error parsing resume with Claude: {str(e)}")
            raise

    def _initialize_resume_data(self):
        """Initialize resume data by loading from cache or parsing."""
        # Check if cached parsed data exists
        if os.path.exists(self.cache_path):
            try:
                with open(self.cache_path, "r") as f:
                    self.resume_data = json.load(f)
                logger.info("Loaded parsed resume data from cache")
                return
            except Exception as e:
                logger.warning(f"Could not load cached resume data: {str(e)}")

        # If no cache, parse the resume
        try:
            logger.info("Parsing resume PDF with Claude...")
            resume_text = self._extract_pdf_text()
            self.resume_data = self._parse_resume_with_claude(resume_text)

            # Save to cache
            with open(self.cache_path, "w") as f:
                json.dump(self.resume_data, f, indent=2)
            logger.info("Successfully parsed and cached resume data")

        except Exception as e:
            logger.error(f"Error initializing resume data: {str(e)}")
            self.resume_data = {"error": "Failed to parse resume"}

    def query_resume(self, query: str) -> str:
        """
        Return the structured resume data as JSON with projects narrative.

        Args:
            query: Not used - kept for compatibility

        Returns:
            JSON string of the structured resume data with projects
        """
        try:
            if not self.resume_data or "error" in self.resume_data:
                return json.dumps({"error": "Resume data not available"})

            # Create a copy of resume data to avoid modifying the cached version
            result_data = self.resume_data.copy()

            # Read projects.md file
            projects_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                "resources",
                "professional",
                "projects.md",
            )

            try:
                with open(projects_path, "r") as f:
                    projects_content = f.read()
                result_data["projectNarratives"] = projects_content
            except Exception as e:
                logger.warning(f"Could not read projects.md: {str(e)}")
                result_data["projectNarratives"] = "Projects file not available"

            return json.dumps(result_data, indent=2)

        except Exception as e:
            error_msg = f"Error accessing resume data: {str(e)}"
            logger.error(error_msg)
            return json.dumps({"error": error_msg})

    def get_tool(self) -> Tool:
        """
        Get the resume info as a LangChain tool.

        Returns:
            A LangChain Tool instance
        """
        return Tool(
            name="resume",
            description=(
                "Get Peter's complete professional resume data as structured JSON. "
                "Returns all information including personal info, technical skills, work experience, education, and publications. "
                "Also includes detailed project narratives from Peter's work history with specific accomplishments and impact. "
                "The agent can then analyze this data to answer specific questions about Peter's background."
            ),
            func=self.query_resume,
            args_schema=ResumeInfoInput,
        )


# Create a singleton instance
resume_info = ResumeInfo()
