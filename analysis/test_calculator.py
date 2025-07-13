#!/usr/bin/env python3
"""Test script for the calculator tool functionality."""

import asyncio
import logging
from artemis.tools.calculator import calculator

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)


def test_calculator():
    """Test various calculator operations."""
    test_cases = [
        "2 + 2",
        "10 * 5",
        "100 / 4",
        "2 ** 8",
        "sqrt(16)",
        "sin(pi/2)",
        "log10(1000)",
        "abs(-42)",
        "round(3.7)",
        "10 / 0",  # Test division by zero
        "invalid expression",  # Test error handling
    ]

    calc = calculator

    print("Testing Calculator Tool")
    print("=" * 50)

    for expression in test_cases:
        result = calc.calculate(expression)
        print(f"{expression:<20} = {result}")

    print("\nTesting LangChain Tool Interface")
    print("=" * 50)

    tool = calc.get_tool()
    print(f"Tool Name: {tool.name}")
    print(f"Tool Description: {tool.description}")

    # Test through tool interface
    result = tool.func("sqrt(144)")
    print(f"\nTool test: sqrt(144) = {result}")


if __name__ == "__main__":
    test_calculator()
