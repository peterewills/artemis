import logging
import os
from typing import Dict, Any
from langchain.tools import Tool
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class ArchitectureInput(BaseModel):
    """Input schema for the architecture tool."""
    query: str = Field(
        default="",
        description="Optional specific query about the architecture (e.g., 'frontend', 'backend', 'deployment', 'tools')"
    )


class ArchitectureInfo:
    """A tool for providing information about Artemis' architecture."""

    def __init__(self):
        self.architecture_file = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "resources",
            "architecture-diagram.md"
        )
        self.architecture_content = self._load_architecture()

    def _load_architecture(self) -> str:
        """Load the architecture diagram and documentation."""
        try:
            if os.path.exists(self.architecture_file):
                with open(self.architecture_file, "r", encoding="utf-8") as f:
                    return f.read()
            else:
                logger.error(f"Architecture file not found: {self.architecture_file}")
                return "Architecture documentation not found."
        except Exception as e:
            logger.error(f"Error loading architecture file: {str(e)}")
            return f"Error loading architecture documentation: {str(e)}"

    def get_architecture_info(self, query: str = "") -> str:
        """
        Return information about Artemis' architecture.
        
        Args:
            query: Optional specific aspect to focus on
            
        Returns:
            Architecture information
        """
        if not self.architecture_content:
            return "Architecture documentation is not available."
        
        # Add context about the query if provided
        if query:
            return f"Query: {query}\n\n{self.architecture_content}"
        else:
            return self.architecture_content

    def get_tool(self) -> Tool:
        """
        Get the architecture info as a LangChain tool.
        
        Returns:
            A LangChain Tool instance
        """
        return Tool(
            name="architecture",
            description=(
                "Provides detailed information about Artemis' architecture, system design, "
                "components, data flow, and deployment. Use this when asked about how Artemis "
                "works, its technical architecture, system components, or deployment details."
            ),
            func=self.get_architecture_info,
            args_schema=ArchitectureInput,
        )


# Create a singleton instance
architecture_info = ArchitectureInfo()