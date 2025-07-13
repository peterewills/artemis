#!/usr/bin/env python3
"""Test the agent with calculator tool."""

import asyncio
import logging
from artemis.chatbot.agent import ArtemisAgent

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


async def test_agent():
    """Test the agent functionality."""
    agent = ArtemisAgent()
    
    # Test 1: Regular conversation
    print("Test 1: Regular conversation")
    print("-" * 50)
    response = await agent.ainvoke([
        ("user", "Hello, what's your name?")
    ])
    print(f"Response: {response}\n")
    
    # Test 2: Tool usage
    print("Test 2: Calculator tool usage")
    print("-" * 50)
    response = await agent.ainvoke([
        ("user", "What is the square root of 144?")
    ])
    print(f"Response: {response}\n")
    
    # Test 3: Streaming with tool
    print("Test 3: Streaming with calculator")
    print("-" * 50)
    async for chunk in agent.astream([
        ("user", "Can you calculate 25 * 4 for me?")
    ]):
        print(chunk, end="", flush=True)
    print("\n")
    
    # Test 4: Conversation history
    print("Test 4: Conversation with history")
    print("-" * 50)
    messages = [
        ("user", "My favorite number is 42"),
        ("assistant", "42 is a great number! It's famously known as the 'Answer to the Ultimate Question of Life, the Universe, and Everything' from The Hitchhiker's Guide to the Galaxy."),
        ("user", "What's my favorite number squared?")
    ]
    response = await agent.ainvoke(messages)
    print(f"Response: {response}\n")


if __name__ == "__main__":
    asyncio.run(test_agent())