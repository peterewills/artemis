import logging
from typing import List, Tuple, AsyncIterator, Dict, Any
from langchain_anthropic import ChatAnthropic
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from langchain_core.messages import BaseMessage
import json

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

        # If we have tools, bind them to the LLM
        if self.tools:
            self.llm_with_tools = self.llm.bind_tools(self.tools)
        else:
            self.llm_with_tools = self.llm

    def _convert_messages(self, messages: List[Tuple[str, str]]) -> List[BaseMessage]:
        """Convert message tuples to LangChain message objects."""
        langchain_messages = []

        for role, content in messages:
            if role == "user":
                langchain_messages.append(HumanMessage(content=content))
            elif role == "assistant":
                langchain_messages.append(AIMessage(content=content))

        return langchain_messages

    def _prepare_messages(self, messages: List[Tuple[str, str]]) -> List[BaseMessage]:
        """Prepare messages with system prompt."""
        langchain_messages = self._convert_messages(messages)
        return [SystemMessage(content=SYSTEM_PROMPT)] + langchain_messages
    
    def _extract_content(self, message) -> str:
        """Extract content from different message formats."""
        if hasattr(message, 'content'):
            content = message.content
            if isinstance(content, list) and content:
                # Handle list format like [{'text': '...', 'type': 'text', 'index': 0}]
                return content[0].get('text', str(content))
            elif isinstance(content, str):
                return content
            else:
                return str(content)
        return str(message)

    async def ainvoke(self, messages: List[Tuple[str, str]]) -> str:
        """Process messages and return a response."""
        full_messages = self._prepare_messages(messages)

        # Invoke LLM with tools
        response = await self.llm_with_tools.ainvoke(full_messages)

        # If there are tool calls, execute them
        if hasattr(response, "tool_calls") and response.tool_calls:
            # Add the assistant's message with tool calls
            full_messages.append(response)

            # Execute each tool call
            for tool_call in response.tool_calls:
                tool_name = tool_call["name"]
                tool_args = tool_call["args"]

                # Find and execute the tool
                for tool in self.tools:
                    if tool.name == tool_name:
                        tool_output = await tool.ainvoke(tool_args)
                        # Add tool result as a message
                        from langchain_core.messages import ToolMessage

                        full_messages.append(
                            ToolMessage(
                                content=str(tool_output), tool_call_id=tool_call["id"]
                            )
                        )
                        break

            # Get final response after tool execution
            final_response = await self.llm_with_tools.ainvoke(full_messages)
            return self._extract_content(final_response)
        else:
            # No tool calls, return direct response
            return self._extract_content(response)

    async def astream(self, messages: List[Tuple[str, str]]) -> AsyncIterator[str]:
        """Stream response tokens with tool support."""
        full_messages = self._prepare_messages(messages)

        # Stream the initial response
        tool_calls = []
        content_started = False
        
        async for chunk in self.llm_with_tools.astream(full_messages):
            # Extract content from chunk
            if hasattr(chunk, "content") and chunk.content:
                # Check if content is a list with text items
                if isinstance(chunk.content, list):
                    for item in chunk.content:
                        if isinstance(item, dict) and item.get("type") == "text":
                            text = item.get("text", "")
                            if text:
                                yield text
                                content_started = True
                elif isinstance(chunk.content, str):
                    yield chunk.content
                    content_started = True
            
            # Collect tool calls if any
            if hasattr(chunk, "tool_call_chunks") and chunk.tool_call_chunks:
                for tool_call_chunk in chunk.tool_call_chunks:
                    if isinstance(tool_call_chunk, dict) and tool_call_chunk.get("index") is not None:
                        index = tool_call_chunk["index"]
                        # Ensure list is large enough
                        while index >= len(tool_calls):
                            tool_calls.append({"name": "", "args": "", "id": ""})

                        if tool_call_chunk.get("name"):
                            tool_calls[index]["name"] = tool_call_chunk["name"]
                        if tool_call_chunk.get("args"):
                            tool_calls[index]["args"] += tool_call_chunk["args"]
                        if tool_call_chunk.get("id"):
                            tool_calls[index]["id"] = tool_call_chunk["id"]

        # If there were tool calls, execute them
        if tool_calls:
            for tool_call in tool_calls:
                if tool_call.get("args"):
                    try:
                        tool_args = json.loads(tool_call["args"])
                    except json.JSONDecodeError:
                        continue

                    tool_name = tool_call["name"]
                    yield f"\n🔧 Using {tool_name} tool"

                    if "expression" in tool_args:
                        yield f": {tool_args['expression']}"
                    yield "...\n"

                    # Find and execute the tool
                    for tool in self.tools:
                        if tool.name == tool_name:
                            tool_output = await tool.ainvoke(tool_args)
                            yield f"📊 Result: {tool_output}\n\n"

                            # Add tool result to messages for final response
                            from langchain_core.messages import ToolMessage

                            # Parse the args if it's a string
                            if isinstance(tool_call.get("args"), str):
                                tool_call["args"] = json.loads(tool_call["args"])
                            
                            full_messages.append(
                                AIMessage(content="", tool_calls=[tool_call])
                            )
                            full_messages.append(
                                ToolMessage(
                                    content=str(tool_output),
                                    tool_call_id=tool_call["id"],
                                )
                            )
                            break

            # Stream final response after tool execution
            async for chunk in self.llm_with_tools.astream(full_messages):
                # Extract content from chunk
                if hasattr(chunk, "content") and chunk.content:
                    # Check if content is a list with text items
                    if isinstance(chunk.content, list):
                        for item in chunk.content:
                            if isinstance(item, dict) and item.get("type") == "text":
                                text = item.get("text", "")
                                if text:
                                    yield text
                    elif isinstance(chunk.content, str):
                        yield chunk.content
