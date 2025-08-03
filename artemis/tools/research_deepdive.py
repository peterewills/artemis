import logging
from typing import Dict, Any, Union, List
from langchain.tools import Tool
from pydantic import BaseModel, Field
import pypdf
import os
import re

logger = logging.getLogger(__name__)


class ResearchDeepDiveInput(BaseModel):
    """Input schema for the research deep dive tool."""

    query: str = Field(
        description="Query about research papers (e.g., 'graph comparison metrics', 'stochastic blockmodel', 'droplet solitons', 'methodology used in [paper]')"
    )
    paper_name: str = Field(
        default="",
        description="Optional: specific paper name to search in. If not provided, searches all papers.",
    )


class ResearchDeepDive:
    """A tool for in-depth querying of research papers."""

    def __init__(self):
        self.research_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "resources",
            "research",
        )
        self.papers = {}
        self.summaries = {}
        self._load_papers()
        self._load_summaries()

    def _load_papers(self):
        """Load and extract text from all research PDFs."""
        try:
            for filename in os.listdir(self.research_dir):
                if filename.endswith(".pdf"):
                    filepath = os.path.join(self.research_dir, filename)
                    try:
                        with open(filepath, "rb") as file:
                            pdf_reader = pypdf.PdfReader(file)
                            text_parts = []
                            for page in pdf_reader.pages:
                                text_parts.append(page.extract_text())
                            paper_name = filename.replace(".pdf", "").replace("-", " ")
                            self.papers[paper_name] = {
                                "filename": filename,
                                "text": "\n".join(text_parts),
                                "pages": len(pdf_reader.pages),
                            }
                            logger.info(f"Successfully loaded paper: {filename}")
                    except Exception as e:
                        logger.error(f"Error loading paper {filename}: {str(e)}")
        except Exception as e:
            logger.error(f"Error accessing research directory: {str(e)}")

    def _load_summaries(self):
        """Load the markdown summaries of research papers."""
        try:
            summary_files = {
                "change-point-detection": "change-point-detection-summary.md",
                "droplet-solitons": "droplet-solitons-summary.md",
                "metrics-for-graph-comparison": "metrics-for-graph-comparison-summary.md",
                "performance-of-test-supermartingale": "performance-of-test-supermartingale-summary.md",
            }

            for paper_key, filename in summary_files.items():
                filepath = os.path.join(self.research_dir, filename)
                if os.path.exists(filepath):
                    try:
                        with open(filepath, "r", encoding="utf-8") as f:
                            self.summaries[paper_key] = f.read()
                            logger.info(f"Successfully loaded summary: {filename}")
                    except Exception as e:
                        logger.error(f"Error loading summary {filename}: {str(e)}")
        except Exception as e:
            logger.error(f"Error loading summaries: {str(e)}")

    def _extract_sections(self, text: str) -> Dict[str, str]:
        """Extract common sections from a research paper."""
        sections = {}
        current_section = "introduction"
        current_content = []

        # Common section headers in research papers
        section_patterns = [
            r"abstract",
            r"introduction",
            r"related\s+work",
            r"background",
            r"methodology",
            r"methods",
            r"approach",
            r"experiments",
            r"results",
            r"discussion",
            r"conclusion",
            r"future\s+work",
            r"references",
            r"appendix",
        ]

        lines = text.split("\n")
        for line in lines:
            line_lower = line.lower().strip()

            # Check if this line is a section header
            is_section = False
            for pattern in section_patterns:
                if re.match(rf"^\d*\.?\s*{pattern}", line_lower) and len(line) < 50:
                    is_section = True
                    if current_content:
                        sections[current_section] = "\n".join(current_content)
                    current_section = pattern.replace(r"\s+", " ")
                    current_content = []
                    break

            if not is_section:
                current_content.append(line)

        # Add the last section
        if current_content:
            sections[current_section] = "\n".join(current_content)

        return sections

    def _search_context(
        self, text: str, query: str, context_lines: int = 5
    ) -> List[str]:
        """Search for query terms and return with context."""
        lines = text.split("\n")
        query_terms = [term.lower() for term in query.split() if len(term) > 2]
        results = []

        for i, line in enumerate(lines):
            line_lower = line.lower()
            if any(term in line_lower for term in query_terms):
                # Get context
                start = max(0, i - context_lines)
                end = min(len(lines), i + context_lines + 1)
                context = lines[start:end]
                results.append("\n".join(context))

        return results

    def query_research(self, query: str, paper_name: str = "") -> str:
        """
        Return research paper summaries for the given query.

        Args:
            query: Question about the research (used for context)
            paper_name: Optional specific paper to search in

        Returns:
            Research paper summaries relevant to the query
        """
        try:
            if not self.summaries:
                return "Error: No research paper summaries loaded"

            # Build context from summaries
            context_parts = []
            
            # Add context about the query
            context_parts.append(f"Query: {query}\n")
            
            if paper_name:
                # Find matching paper summary
                matched = False
                for key, summary in self.summaries.items():
                    if paper_name.lower() in key.lower():
                        context_parts.append(f"Paper Summary for '{key}':\n{summary}")
                        matched = True
                        break
                if not matched:
                    return f"Paper '{paper_name}' not found. Available papers: {', '.join(self.summaries.keys())}"
            else:
                # Include all summaries
                context_parts.append(
                    "Research Paper Summaries (Peter Wills' Research):\n"
                )
                context_parts.append(
                    "Note: Peter's primary research focus is on graph/network analysis, "
                    "particularly the two papers on Change Point Detection in a Dynamic Stochastic Blockmodel "
                    "and Metrics for Graph Comparison.\n"
                )
                for key, summary in self.summaries.items():
                    context_parts.append(f"\n=== {key.replace('-', ' ').title()} ===\n{summary}\n")

            return "\n".join(context_parts)

        except Exception as e:
            error_msg = f"Error loading research summaries: {str(e)}"
            logger.error(error_msg)
            return error_msg

    def list_papers(self) -> str:
        """List all available research papers."""
        paper_list = []

        if self.summaries:
            paper_list.append("Papers with summaries available:")
            for name in self.summaries.keys():
                paper_list.append(f"- {name}")

        if self.papers:
            paper_list.append("\nFull PDFs loaded:")
            for name, info in self.papers.items():
                paper_list.append(f"- {name} ({info['pages']} pages)")

        if not paper_list:
            return "No research papers or summaries loaded"

        return "\n".join(paper_list)

    def get_tool(self) -> Tool:
        """
        Get the research deep dive as a LangChain tool.

        Returns:
            A LangChain Tool instance
        """
        return Tool(
            name="research",
            description=(
                "Retrieves research paper summaries about Peter Wills' academic work. "
                "Returns summaries of Peter's research papers for context injection. "
                "Can return all paper summaries or focus on a specific paper. "
                "Use this tool to get research context that will be used to answer questions. "
                "Example queries: 'tell me about Peter's research', 'graph comparison metrics', "
                "'what is a droplet soliton', 'research interests', 'publications'"
            ),
            func=lambda query, paper_name="": self.query_research(query, paper_name),
            args_schema=ResearchDeepDiveInput,
        )


# Create a singleton instance
research_deepdive = ResearchDeepDive()
