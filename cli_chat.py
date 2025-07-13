#!/usr/bin/env python3
"""
Command line interface for testing the Artemis chatbot locally.
"""
import asyncio
import logging
import sys
from typing import List, Tuple

from artemis.chatbot.agent import ArtemisAgent
from artemis.config import settings

# Set up logging
logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


class CLIChatInterface:
    """Simple command line interface for the chatbot."""

    def __init__(self):
        self.chatbot = ArtemisAgent()
        self.conversation_history: List[Tuple[str, str]] = []

    def print_welcome(self):
        """Print welcome message."""
        print("\n" + "=" * 60)
        print("🤖 Welcome to Artemis - Personal AI Assistant")
        print("=" * 60)
        print("Ask me anything about Peter Wills!")
        print("Commands:")
        print("  - Type 'exit' or 'quit' to end the conversation")
        print("  - Type 'clear' to clear conversation history")
        print("  - Type 'history' to see conversation history")
        print("  - Type 'stream' to toggle streaming mode")
        print("-" * 60)

    def print_separator(self):
        """Print a separator line."""
        print("-" * 60)

    def show_history(self):
        """Show conversation history."""
        if not self.conversation_history:
            print("No conversation history yet.")
            return

        print("\n📜 Conversation History:")
        for i, (role, content) in enumerate(self.conversation_history, 1):
            role_emoji = "👤" if role == "user" else "🤖"
            print(
                f"{i}. {role_emoji} {role.title()}: {content[:100]}{'...' if len(content) > 100 else ''}"
            )

    def clear_history(self):
        """Clear conversation history."""
        self.conversation_history = []
        print("✅ Conversation history cleared.")

    async def get_response(self, user_input: str, stream: bool = True) -> str:
        """Get response from chatbot."""
        # Add user message to history
        self.conversation_history.append(("user", user_input))

        try:
            if stream:
                print("🤖 Artemis: ", end="", flush=True)
                response_parts = []
                async for chunk in self.chatbot.astream(self.conversation_history):
                    print(chunk, end="", flush=True)
                    response_parts.append(chunk)
                print()  # New line after streaming
                response = "".join(response_parts)
            else:
                print("🤖 Artemis is thinking...")
                response = await self.chatbot.ainvoke(self.conversation_history)
                print(f"🤖 Artemis: {response}")

            # Add assistant response to history
            self.conversation_history.append(("assistant", response))
            return response

        except Exception as e:
            error_msg = f"❌ Error: {str(e)}"
            print(error_msg)
            return error_msg

    async def run(self):
        """Run the interactive chat interface."""
        self.print_welcome()

        streaming_mode = True

        while True:
            try:
                # Get user input
                user_input = input("\n👤 You: ").strip()

                # Handle commands
                if user_input.lower() in ["exit", "quit"]:
                    print("👋 Goodbye!")
                    break
                elif user_input.lower() == "clear":
                    self.clear_history()
                    continue
                elif user_input.lower() == "history":
                    self.show_history()
                    continue
                elif user_input.lower() == "stream":
                    streaming_mode = not streaming_mode
                    status = "enabled" if streaming_mode else "disabled"
                    print(f"✅ Streaming mode {status}")
                    continue
                elif not user_input:
                    print("Please enter a message or command.")
                    continue

                # Get and display response
                await self.get_response(user_input, stream=streaming_mode)

            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except EOFError:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Unexpected error: {e}")


async def main():
    """Main entry point."""
    # Check if API key is configured
    if not settings.anthropic_api_key:
        print("❌ Error: ANTHROPIC_API_KEY environment variable is not set.")
        print("Please set it with: export ANTHROPIC_API_KEY='your-api-key'")
        sys.exit(1)

    # Run the chat interface
    interface = CLIChatInterface()
    await interface.run()


if __name__ == "__main__":
    asyncio.run(main())
