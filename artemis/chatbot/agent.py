import logging
from typing import List, Tuple, AsyncIterator, Dict, Any
from langchain_anthropic import ChatAnthropic
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import Runnable
from langchain_core.messages import ToolMessage

from artemis.config import settings
from artemis.chatbot.prompt import SYSTEM_PROMPT
from artemis.chatbot.tools import get_tools

logger = logging.getLogger(__name__)


class ArtemisAgent:
    def __init__(self):
        self.llm = ChatAnthropic(
            anthropic_api_key=settings.anthropic_api_key,
            model_name=settings.model_name,
            temperature=settings.temperature,
            max_tokens=settings.max_tokens,
            streaming=True,
        )

        # Get available tools
        self.tools = get_tools()

        # Create the prompt template
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", SYSTEM_PROMPT),
                MessagesPlaceholder(variable_name="messages"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        )

        # Create the agent
        if self.tools:
            # Bind tools to the LLM
            llm_with_tools = self.llm.bind_tools(self.tools)
            agent = create_tool_calling_agent(llm_with_tools, self.tools, prompt)
            self.agent_executor = AgentExecutor(
                agent=agent,
                tools=self.tools,
                verbose=True,
                handle_parsing_errors=True,
                return_intermediate_steps=True,
            )
        else:
            # No tools, use regular LLM
            self.agent_executor = None

    def _convert_messages(self, messages: List[Tuple[str, str]]) -> List:
        """Convert message tuples to LangChain message objects."""
        langchain_messages = []

        for role, content in messages:
            if role == "user":
                langchain_messages.append(HumanMessage(content=content))
            elif role == "assistant":
                langchain_messages.append(AIMessage(content=content))

        return langchain_messages

    async def ainvoke(self, messages: List[Tuple[str, str]]) -> str:
        """Process messages and return a response."""
        langchain_messages = self._convert_messages(messages)

        if self.agent_executor:
            # Use agent with tools
            response = await self.agent_executor.ainvoke(
                {"messages": langchain_messages}
            )
            return response["output"]
        else:
            # No tools, use regular LLM
            full_messages = [SystemMessage(content=SYSTEM_PROMPT)] + langchain_messages
            response = await self.llm.ainvoke(full_messages)
            return response.content

    async def astream(self, messages: List[Tuple[str, str]]) -> AsyncIterator[str]:
        """Stream response tokens with tool support."""
        langchain_messages = self._convert_messages(messages)

        if self.agent_executor:
            # Stream with tools support
            async for event in self.agent_executor.astream_events(
                {"messages": langchain_messages}, version="v2"
            ):
                kind = event["event"]

                if kind == "on_chat_model_stream":
                    # Stream content from the model
                    content = event["data"]["chunk"].content
                    if content:
                        yield content
                elif kind == "on_tool_start":
                    # Tool is being called
                    tool_name = event["name"]
                    tool_input = event["data"].get("input", {})
                    yield f"\n🔧 Using {tool_name} tool"
                    if isinstance(tool_input, dict) and "expression" in tool_input:
                        yield f": {tool_input['expression']}"
                    yield "...\n"
                elif kind == "on_tool_end":
                    # Tool finished
                    output = event["data"].get("output", "")
                    if output:
                        yield f"📊 Result: {output}\n\n"
        else:
            # No tools, regular streaming
            full_messages = [SystemMessage(content=SYSTEM_PROMPT)] + langchain_messages
            async for chunk in self.llm.astream(full_messages):
                if chunk.content:
                    yield chunk.content
