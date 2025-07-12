import logging
from typing import List, Tuple, AsyncIterator
from langchain_anthropic import ChatAnthropic
from langchain.schema import HumanMessage, AIMessage, SystemMessage

from artemis.config import settings
from artemis.chatbot.prompt import SYSTEM_PROMPT

logger = logging.getLogger(__name__)


class ArtemisChatbot:
    def __init__(self):
        self.llm = ChatAnthropic(
            anthropic_api_key=settings.anthropic_api_key,
            model_name=settings.model_name,
            temperature=settings.temperature,
            max_tokens=settings.max_tokens,
            streaming=True,
        )
    
    def _convert_messages(self, messages: List[Tuple[str, str]]) -> List:
        """Convert message tuples to LangChain message objects."""
        langchain_messages = []
        
        # Add system message at the beginning
        langchain_messages.append(SystemMessage(content=SYSTEM_PROMPT))
        
        for role, content in messages:
            if role == "user":
                langchain_messages.append(HumanMessage(content=content))
            elif role == "assistant":
                langchain_messages.append(AIMessage(content=content))
                
        return langchain_messages
    
    async def ainvoke(self, messages: List[Tuple[str, str]]) -> str:
        """Process messages and return a response."""
        langchain_messages = self._convert_messages(messages)
        
        response = await self.llm.ainvoke(langchain_messages)
        return response.content
    
    async def astream(self, messages: List[Tuple[str, str]]) -> AsyncIterator[str]:
        """Stream response tokens."""
        langchain_messages = self._convert_messages(messages)
        
        async for chunk in self.llm.astream(langchain_messages):
            if chunk.content:
                yield chunk.content