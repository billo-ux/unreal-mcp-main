"""
UI Tools for Unreal MCP.

Best Practices (Cursor Rules):
- Do not use Any, object, Optional, or Union types for parameters.
- Use explicit types for all parameters; handle defaults inside the function.
- Every @mcp.tool method must have a docstring with at least one usage example.
- Always return a dict with 'success' and a clear message or result.
- Handle errors robustly and log them.

Example usage for each tool is provided in the docstring.
"""

import logging
from typing import Dict, List
from mcp.server.fastmcp import FastMCP, Context
from unreal_mcp_server import get_unreal_connection

logger = logging.getLogger("UnrealMCP")

def register_ui_tools(mcp: FastMCP):
    """Register UI tools with the MCP server."""
    # ... (tools will be added here in subsequent steps)

    @mcp.tool()
    def create_umg_widget_blueprint(ctx: Context, widget_name: str, save_path: str = "/Game/UI") -> Dict[str, str]:
        """
        Create a UMG Widget Blueprint.
        Args:
            widget_name: Name of the widget blueprint
            save_path: Path to save the widget blueprint
        Returns:
            Dict with success status and asset path
        Example:
            create_umg_widget_blueprint(ctx, widget_name="MyWidget", save_path="/Game/UI")
        """
        try:
            params = {"widget_name": widget_name, "save_path": save_path}
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            response = unreal.send_command("create_umg_widget_blueprint", params)
            return response or {"success": False, "message": "No response from Unreal Engine"}
        except Exception as e:
            logger.error(f"Error creating UMG widget blueprint: {e}")
            return {"success": False, "message": str(e)}

    @mcp.tool()
    def add_text_block_to_widget(ctx: Context, widget_name: str, text: str, block_name: str = "TextBlock", position: List[int] = None) -> Dict[str, str]:
        """
        Add a text block to a UMG widget.
        Args:
            widget_name: Name of the widget blueprint
            text: Text to display
            block_name: Name of the text block (default: 'TextBlock')
            position: [X, Y] position in the widget (default: [0, 0])
        Returns:
            Dict with success status
        Example:
            add_text_block_to_widget(ctx, widget_name="MyWidget", text="Hello", block_name="Title", position=[10, 10])
        """
        try:
            if position is None:
                position = [0, 0]
            params = {"widget_name": widget_name, "text": text, "block_name": block_name, "position": position}
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            response = unreal.send_command("add_text_block_to_widget", params)
            return response or {"success": False, "message": "No response from Unreal Engine"}
        except Exception as e:
            logger.error(f"Error adding text block: {e}")
            return {"success": False, "message": str(e)}

    @mcp.tool()
    def add_button_to_widget(ctx: Context, widget_name: str, button_name: str = "Button", position: List[int] = None) -> Dict[str, str]:
        """
        Add a button to a UMG widget.
        Args:
            widget_name: Name of the widget blueprint
            button_name: Name of the button (default: 'Button')
            position: [X, Y] position in the widget (default: [0, 0])
        Returns:
            Dict with success status
        Example:
            add_button_to_widget(ctx, widget_name="MyWidget", button_name="PlayButton", position=[20, 20])
        """
        try:
            if position is None:
                position = [0, 0]
            params = {"widget_name": widget_name, "button_name": button_name, "position": position}
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            response = unreal.send_command("add_button_to_widget", params)
            return response or {"success": False, "message": "No response from Unreal Engine"}
        except Exception as e:
            logger.error(f"Error adding button: {e}")
            return {"success": False, "message": str(e)}

    @mcp.tool()
    def bind_widget_event(ctx: Context, widget_name: str, element_name: str, event_name: str, handler_function: str) -> Dict[str, str]:
        """
        Bind an event to a widget element.
        Args:
            widget_name: Name of the widget blueprint
            element_name: Name of the UI element (e.g., button)
            event_name: Name of the event (e.g., 'OnClicked')
            handler_function: Name of the function to call
        Returns:
            Dict with success status
        Example:
            bind_widget_event(ctx, widget_name="MyWidget", element_name="PlayButton", event_name="OnClicked", handler_function="OnPlayClicked")
        """
        try:
            params = {"widget_name": widget_name, "element_name": element_name, "event_name": event_name, "handler_function": handler_function}
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            response = unreal.send_command("bind_widget_event", params)
            return response or {"success": False, "message": "No response from Unreal Engine"}
        except Exception as e:
            logger.error(f"Error binding widget event: {e}")
            return {"success": False, "message": str(e)}

    @mcp.tool()
    def add_widget_to_viewport(ctx: Context, widget_name: str) -> Dict[str, str]:
        """
        Add a widget to the viewport.
        Args:
            widget_name: Name of the widget blueprint
        Returns:
            Dict with success status
        Example:
            add_widget_to_viewport(ctx, widget_name="MyWidget")
        """
        try:
            params = {"widget_name": widget_name}
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            response = unreal.send_command("add_widget_to_viewport", params)
            return response or {"success": False, "message": "No response from Unreal Engine"}
        except Exception as e:
            logger.error(f"Error adding widget to viewport: {e}")
            return {"success": False, "message": str(e)}

    @mcp.tool()
    def set_text_block_binding(ctx: Context, widget_name: str, block_name: str, binding_function: str) -> Dict[str, str]:
        """
        Set a binding for a text block in a widget.
        Args:
            widget_name: Name of the widget blueprint
            block_name: Name of the text block
            binding_function: Name of the function to bind
        Returns:
            Dict with success status
        Example:
            set_text_block_binding(ctx, widget_name="MyWidget", block_name="Title", binding_function="GetTitleText")
        """
        try:
            params = {"widget_name": widget_name, "block_name": block_name, "binding_function": binding_function}
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            response = unreal.send_command("set_text_block_binding", params)
            return response or {"success": False, "message": "No response from Unreal Engine"}
        except Exception as e:
            logger.error(f"Error setting text block binding: {e}")
            return {"success": False, "message": str(e)}

    @mcp.tool()
    def set_widget_parent(ctx: Context, widget_name: str, parent_name: str) -> Dict[str, str]:
        """
        Set the parent of a widget for dynamic hierarchy management.
        Args:
            widget_name: Name of the widget to reparent
            parent_name: Name of the new parent widget
        Returns:
            Dict with success status and message
        Example:
            set_widget_parent(ctx, widget_name="ChildWidget", parent_name="ParentWidget")
        """
        try:
            params = {"widget_name": widget_name, "parent_name": parent_name}
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            response = unreal.send_command("set_widget_parent", params)
            return response or {"success": False, "message": "No response from Unreal Engine"}
        except Exception as e:
            logger.error(f"Error setting widget parent: {e}")
            return {"success": False, "message": str(e)}

    @mcp.tool()
    def reorder_widget(ctx: Context, widget_name: str, new_index: int) -> Dict[str, str]:
        """
        Reorder a widget within its parent container.
        Args:
            widget_name: Name of the widget to reorder
            new_index: New index/position within the parent
        Returns:
            Dict with success status and message
        Example:
            reorder_widget(ctx, widget_name="MyButton", new_index=1)
        """
        # TODO: Implement widget reordering
        return {"success": False, "message": "Not yet implemented"}

    @mcp.tool()
    def remove_widget_from_parent(ctx: Context, widget_name: str) -> Dict[str, str]:
        """
        Remove a widget from its parent container.
        Args:
            widget_name: Name of the widget to remove
        Returns:
            Dict with success status and message
        Example:
            remove_widget_from_parent(ctx, widget_name="MyTextBlock")
        """
        # TODO: Implement widget removal
        return {"success": False, "message": "Not yet implemented"}

    @mcp.tool()
    def get_widget_hierarchy(ctx: Context, widget_name: str) -> Dict[str, object]:
        """
        Get the hierarchy (parent and children) of a widget.
        Args:
            widget_name: Name of the widget to query
        Returns:
            Dict with parent and children widget names
        Example:
            get_widget_hierarchy(ctx, widget_name="MyPanel")
        """
        # TODO: Implement widget hierarchy query
        return {"success": False, "parent": None, "children": []} 