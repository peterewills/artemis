from typing import List
from langchain.tools import Tool
from artemis.tools.calculator import calculator


def get_tools() -> List[Tool]:
    """Return list of available tools for the chatbot."""
    tools = []

    # Add calculator tool for testing
    tools.append(calculator.get_tool())

    # Example of how to add a tool later:
    # tools.append(Tool(
    #     name="get_resume_details",
    #     description="Get specific details from Peter's resume",
    #     func=get_resume_details
    # ))

    return tools
