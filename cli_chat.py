#!/usr/bin/env python3
"""
Command line interface for testing the Artemis chatbot locally.
"""
import asyncio
import logging
import sys
import os
from typing import List, Tuple

# Enable command history with arrow keys
try:
    import readline
except ImportError:
    # readline might not be available on Windows
    pass

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

        # Set up readline for command history
        self.history_file = os.path.expanduser("~/.artemis_history")
        self._setup_readline()

    def _setup_readline(self):
        """Set up readline for better terminal experience."""
        try:
            import readline

            # Enable tab completion (though we don't define completions yet)
            readline.parse_and_bind("tab: complete")

            # Set history file
            try:
                readline.read_history_file(self.history_file)
            except FileNotFoundError:
                pass

            # Set history length
            readline.set_history_length(1000)

            # Save history on exit
            import atexit
            atexit.register(readline.write_history_file, self.history_file)

        except ImportError:
            # readline not available
            pass

    def print_welcome(self):
        """Print welcome message."""
        ascii_art = """
 ░▒▓██████▓▒░░▒▓███████▓▒░▒▓████████▓▒░▒▓████████▓▒░▒▓██████████████▓▒░░▒▓█▓▒░░▒▓███████▓▒░
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░   ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓█▓▒░
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░   ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓█▓▒░
░▒▓████████▓▒░▒▓███████▓▒░  ░▒▓█▓▒░   ░▒▓██████▓▒░ ░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓██████▓▒░
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░   ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░   ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░   ░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓███████▓▒░
"""

        splash_message = """
 Agentic Research & Tool-Enhanced Machine Intelligence System
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ARTEMIS is an AI agent that leverages multiple tools and data sources
to provide comprehensive information about Dr. Peter Wills.

Available capabilities:
 • Professional background analysis
 • Technical expertise assessment
 • Project portfolio exploration
 • Real-time information synthesis

CLI Commands:
 • 'exit' or 'quit' - End the conversation
 • 'clear' - Clear conversation history
 • 'history' - Show conversation history
 • 'stream' - Toggle streaming mode
 • Use ↑/↓ arrows for command history

Type your query and press Enter to begin.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

        print(ascii_art)
        print(splash_message)

    def print_separator(self):
        """Print a separator line."""
        print("━" * 60)

    def show_history(self):
        """Show conversation history."""
        if not self.conversation_history:
            print("\nNo conversation history yet.")
            return

        print("\nConversation History:")
        print("━" * 60)
        for i, (role, content) in enumerate(self.conversation_history, 1):
            role_label = "You" if role == "user" else "Artemis"
            print(f"\n{i}. {role_label}:")
            print(f"   {content[:100]}{'...' if len(content) > 100 else ''}")
        print("━" * 60)

    def clear_history(self):
        """Clear conversation history."""
        self.conversation_history = []
        print("\n✓ Conversation history cleared.")

    async def get_response(self, user_input: str, stream: bool = True) -> str:
        """Get response from chatbot."""
        # Add user message to history
        self.conversation_history.append(("user", user_input))

        try:
            if stream:
                response_parts = []
                async for chunk in self.chatbot.astream(self.conversation_history):
                    print(chunk, end="", flush=True)
                    response_parts.append(chunk)
                print("\n")  # New line after streaming
                response = "".join(response_parts)
            else:
                response = await self.chatbot.ainvoke(self.conversation_history)
                print(response)

            # Add assistant response to history
            self.conversation_history.append(("assistant", response))
            return response

        except Exception as e:
            error_msg = f"\nError: {str(e)}\n"
            print(error_msg)
            return error_msg

    async def run(self):
        """Run the interactive chat interface."""
        self.print_welcome()

        streaming_mode = True

        while True:
            try:
                # Get user input with simple prompt
                user_input = input("\n> ").strip()

                # Handle commands
                if user_input.lower() in ["exit", "quit"]:
                    print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
                    print("Thank you for using ARTEMIS. Goodbye!")
                    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
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
                    print(f"\n✓ Streaming mode {status}.")
                    continue
                elif not user_input:
                    continue

                # Get and display response
                await self.get_response(user_input, stream=streaming_mode)

            except KeyboardInterrupt:
                print("\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
                print("Thank you for using ARTEMIS. Goodbye!")
                print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
                break
            except EOFError:
                print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
                print("Thank you for using ARTEMIS. Goodbye!")
                print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
                break
            except Exception as e:
                print(f"\n⚠ Unexpected error: {e}")


async def main():
    """Main entry point."""
    # Check if API key is configured
    if not settings.anthropic_api_key:
        print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("⚠ Error: ANTHROPIC_API_KEY environment variable is not set.")
        print("\nPlease set it with: export ANTHROPIC_API_KEY='your-api-key'")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
        sys.exit(1)

    # Run the chat interface
    interface = CLIChatInterface()
    await interface.run()


if __name__ == "__main__":
    asyncio.run(main())
