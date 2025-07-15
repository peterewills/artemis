import logging
from langchain.tools import Tool
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class PersonalInput(BaseModel):
    """Input schema for the personal info tool."""

    query: str = Field(
        description="Not used - the tool returns complete personal info regardless of input. Kept for compatibility."
    )


def get_personal_info():
    return """
I grew up in Rochester, NY. I went to Brighton High School and graduated in 2006.

I have a bachelors degree in Physics from Reed College, where I did
my thesis on measurement of quantum entanglement in optical systems.

After graduating from Reed, I spent two years living at Great Vow Zen Monastery in
Clatskanie, OR. There, I followed a daily schedule of work and meditation, and did
frequent silent retreats. Meditation is still a large part of my life, and I continue to
attend weeklong silent retreats four times a year.

After the monastery, I began working on my Ph.D. in Applied Mathematics at University of
Colorado. My dissertation focused on network analysis; you can learn more by asking
about my research. During the course of my graduate studies, it became clear I was more
interested in building stuff than in doing research. I fell in love with Python (and
Scala, and Haskell, and emacs) and so when I was done with my degree it was obvious I
wanted to go into industry.

After a brief stint in Denver, I spent some years working in the San Francisco tech
sector. I moved back East during the pandemic. I now live in Rochester, and am lucky to
spend a lot of time with my sister and her kids, as well as very old friends.

I am a passionate cyclist; I enjoy going on very long bike rides, sometimes riding
through the night. I also enjoy building bicycles, and have fabricated two frames
myself. In my free time, if I'm not spendint time with friends and family, I'm generall
out on my bike.

I have two cats that I love very much. Their names are Momo and Porgy.

Personally, my strengths are my ability to execute and a keen eye for rapidly
understanding and disentangling complex systems. My weaknesses are my impatience and my
tendency to become apathetic when I am disconnected from the 'why' of a task.
    """


class PersonalInfo:
    """A tool for providing Peter's personal background information."""

    def __init__(self):
        pass

    def get_personal_info_text(self, query: str) -> str:
        """
        Return Peter's personal background information.

        Args:
            query: Not used - kept for compatibility

        Returns:
            String containing Peter's personal background information
        """
        try:
            personal_info = get_personal_info()
            logger.info("Retrieved personal information")
            return personal_info.strip()

        except Exception as e:
            error_msg = f"Error accessing personal info: {str(e)}"
            logger.error(error_msg)
            return error_msg

    def get_tool(self) -> Tool:
        """
        Get the personal info as a LangChain tool.

        Returns:
            A LangChain Tool instance
        """
        return Tool(
            name="personal",
            description=(
                "Get Peter's personal background information including his upbringing, education, "
                "life experiences, interests, and personal qualities. Use this tool when someone "
                "asks about Peter generally or his qualities as a human being."
            ),
            func=self.get_personal_info_text,
            args_schema=PersonalInput,
        )


# Create a singleton instance
personal_info = PersonalInfo()
