"""
Minimal FastMCP and Context classes for MCP tool registration and context passing.
This is a stub implementation to resolve import errors and allow tool modules to function.
"""
from typing import Callable, Any, Dict

class Context:
    """
    Context object passed to MCP tools. Extend as needed for your project.
    """
    def __init__(self, user: str = "", session: str = ""):
        self.user = user
        self.session = session

class FastMCP:
    """
    Minimal MCP server class for registering tools.
    """
    def __init__(self):
        self.tools: Dict[str, Callable] = {}

    def tool(self):
        """
        Decorator to register a function as an MCP tool.
        Usage:
            @mcp.tool()
            def my_tool(ctx: Context, ...):
                ...
        """
        def decorator(func: Callable) -> Callable:
            self.tools[func.__name__] = func
            return func
        return decorator 