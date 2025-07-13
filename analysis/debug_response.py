#!/usr/bin/env python3
"""Debug the response format from Anthropic."""

import asyncio
from artemis.chatbot.agent import ArtemisAgent


async def debug_response():
    """Debug response format."""
    agent = ArtemisAgent()
    
    # Get the raw response
    full_messages = agent._prepare_messages([("user", "Hello")])
    response = await agent.llm_with_tools.ainvoke(full_messages)
    
    print("Response type:", type(response))
    print("Response:", response)
    
    if hasattr(response, '__dict__'):
        print("Response attributes:", response.__dict__)
    
    # Try streaming
    print("\nStreaming chunks:")
    async for chunk in agent.llm_with_tools.astream(full_messages):
        print("Chunk type:", type(chunk))
        print("Chunk:", chunk)
        if hasattr(chunk, '__dict__'):
            print("Chunk attributes:", chunk.__dict__)
        break  # Just check first chunk


if __name__ == "__main__":
    asyncio.run(debug_response())