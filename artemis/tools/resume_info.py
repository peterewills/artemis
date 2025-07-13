import logging
import json
import os
from typing import Dict, Any, Optional
from langchain.tools import Tool
from pydantic import BaseModel, Field
import pypdf
from langchain_anthropic import ChatAnthropic
from langchain.schema import HumanMessage, SystemMessage

logger = logging.getLogger(__name__)


class ResumeInfoInput(BaseModel):
    """Input schema for the resume info tool."""

    query: str = Field(
        description="Query about professional history (e.g., 'current position', 'education', 'work experience', 'skills', 'publications')"
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
        Query information from the structured resume data using Claude.

        Args:
            query: Question about professional history

        Returns:
            Claude's answer based on the resume data
        """
        try:
            # Check if this is a research-related query
            research_keywords = ['research', 'papers', 'publications',
                               'graph', 'network', 'blockmodel', 'supermartingale', 'droplet', 'soliton']
            query_lower = query.lower()

            if any(keyword in query_lower for keyword in research_keywords):
                return ("This query appears to be about research. Please use the research tool "
                       "for questions about Peter's research papers and academic work. The resume tool "
                       "is for professional experience, education, and skills information.")

            if not self.resume_data or "error" in self.resume_data:
                return "Error: Resume data not available"

            # Initialize Claude for answering queries
            llm = ChatAnthropic(
                model="claude-sonnet-4-20250514",
                temperature=0,
                max_tokens=4096,
            )

            # Create the prompt with resume context
            system_prompt = """You are a helpful assistant answering questions about Peter Wills' professional background based on his resume data.
Be concise and direct in your answers. Use the structured resume data provided to answer questions accurately.
If the information requested is not in the resume data, say so clearly."""

            user_prompt = f"""Here is Peter Wills' resume in JSON format:

{json.dumps(self.resume_data, indent=2)}

Question: {query}

Please answer based on the resume data above."""

            # Make the API call
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt),
            ]
            response = llm.invoke(messages)

            return response.content

        except Exception as e:
            error_msg = f"Error querying resume: {str(e)}"
            logger.error(error_msg)
            return error_msg

    def get_tool(self) -> Tool:
        """
        Get the resume info as a LangChain tool.

        Returns:
            A LangChain Tool instance
        """
        return Tool(
            name="resume",
            description=(
                "Query structured information from Peter's professional resume. "
                "Ask about current position, work experience, education, skills, contact info, etc. "
                "NOT for research papers or research content - use research tool instead. "
                "Example queries: 'current position', 'education background', 'technical skills', 'work experience'"
            ),
            func=self.query_resume,
            args_schema=ResumeInfoInput,
        )


# Create a singleton instance
resume_info = ResumeInfo()
