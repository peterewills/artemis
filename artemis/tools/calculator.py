import logging
from typing import Dict, Any, Union
from langchain.tools import Tool
from pydantic import BaseModel, Field
import math
import operator

logger = logging.getLogger(__name__)


class CalculatorInput(BaseModel):
    """Input schema for the calculator tool."""

    expression: str = Field(
        description="Mathematical expression to evaluate (e.g., '2 + 2', '10 * 5', 'sqrt(16)')"
    )


class Calculator:
    """A calculator tool for basic and advanced mathematical operations."""

    def __init__(self):
        self.operators = {
            "+": operator.add,
            "-": operator.sub,
            "*": operator.mul,
            "/": operator.truediv,
            "**": operator.pow,
            "^": operator.pow,
            "%": operator.mod,
        }

        self.functions = {
            "sqrt": math.sqrt,
            "sin": math.sin,
            "cos": math.cos,
            "tan": math.tan,
            "log": math.log,
            "log10": math.log10,
            "exp": math.exp,
            "abs": abs,
            "round": round,
            "floor": math.floor,
            "ceil": math.ceil,
        }

    def calculate(self, expression: str) -> Union[float, int, str]:
        """
        Evaluate a mathematical expression safely.

        Args:
            expression: Mathematical expression to evaluate

        Returns:
            The result of the calculation or an error message
        """
        try:
            # Remove whitespace
            expression = expression.strip()

            # Create a safe namespace with math functions
            safe_namespace = {"pi": math.pi, "e": math.e, **self.functions}

            # Evaluate the expression
            result = eval(expression, {"__builtins__": {}}, safe_namespace)

            # Format the result nicely
            if isinstance(result, float) and result.is_integer():
                result = int(result)

            logger.info(f"Calculated: {expression} = {result}")
            return result

        except ZeroDivisionError:
            error_msg = "Error: Division by zero"
            logger.error(f"{error_msg} in expression: {expression}")
            return error_msg
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            logger.error(f"{error_msg} in expression: {expression}")
            return error_msg

    def get_tool(self) -> Tool:
        """
        Get the calculator as a LangChain tool.

        Returns:
            A LangChain Tool instance
        """
        return Tool(
            name="calculator",
            description=(
                "Useful for performing mathematical calculations. "
                "Supports basic operations (+, -, *, /, **, %) and "
                "functions (sqrt, sin, cos, tan, log, exp, abs, round, floor, ceil). "
                "Example inputs: '2 + 2', 'sqrt(16)', 'sin(pi/2)', '10 ** 2'"
            ),
            func=lambda expression: str(self.calculate(expression)),
            args_schema=CalculatorInput,
        )


# Create a singleton instance
calculator = Calculator()
