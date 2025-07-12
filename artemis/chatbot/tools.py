from typing import List
from langchain.tools import Tool


def get_tools() -> List[Tool]:
    """Return list of available tools for the chatbot."""
    # Start with no tools - we can add them later
    tools = []
    
    # Example of how to add a tool later:
    # tools.append(Tool(
    #     name="get_resume_details",
    #     description="Get specific details from Peter's resume",
    #     func=get_resume_details
    # ))
    
    return tools