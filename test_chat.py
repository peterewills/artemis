#!/usr/bin/env python3
"""Simple test script for the Artemis chatbot API."""
import asyncio
import aiohttp
import json
import sys


async def test_streaming():
    """Test the streaming chat endpoint."""
    url = "http://localhost:8000/api/chat"

    messages = [{"role": "user", "content": "Tell me about Peter Wills"}]

    payload = {"messages": messages, "stream": True}

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as response:
            print("Streaming response:")
            print("-" * 50)

            async for line in response.content:
                if line:
                    decoded = line.decode("utf-8").strip()
                    if decoded.startswith("data:"):
                        data = decoded[5:].strip()
                        if data:
                            try:
                                chunk = json.loads(data)
                                if chunk.get("type") == "token":
                                    print(chunk["content"], end="", flush=True)
                                elif chunk.get("type") == "error":
                                    print(f"\nError: {chunk['content']}")
                                elif chunk.get("type") == "done":
                                    print("\n\nStream completed.")
                            except json.JSONDecodeError:
                                pass


async def test_non_streaming():
    """Test the non-streaming chat endpoint."""
    url = "http://localhost:8000/api/chat"

    messages = [{"role": "user", "content": "What kind of work does Peter do?"}]

    payload = {"messages": messages, "stream": False}

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as response:
            result = await response.json()
            print("\nNon-streaming response:")
            print("-" * 50)
            print(result.get("response", "No response"))


async def main():
    print("Testing Artemis Chatbot API...")

    # Test health endpoint first
    async with aiohttp.ClientSession() as session:
        async with session.get("http://localhost:8000/health") as response:
            if response.status != 200:
                print("Server is not running. Start it with: poetry run python run.py")
                sys.exit(1)
            print("Server is healthy!")

    # Run tests
    await test_streaming()
    print("\n" + "=" * 50 + "\n")
    await test_non_streaming()


if __name__ == "__main__":
    asyncio.run(main())
