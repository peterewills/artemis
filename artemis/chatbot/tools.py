from typing import List
from langchain.tools import Tool
from artemis.tools.resume_info import resume_info
from artemis.tools.research_deepdive import research_deepdive
from artemis.tools.personal import personal_info
from artemis.tools.architecture import architecture_info


def get_tools() -> List[Tool]:
    """Return list of available tools for the chatbot."""
    tools = []

    # Add resume info tool
    tools.append(resume_info.get_tool())

    # Add research deep dive tool
    tools.append(research_deepdive.get_tool())

    # Add personal info tool
    tools.append(personal_info.get_tool())

    # Add architecture info tool
    tools.append(architecture_info.get_tool())

    return tools
