"""
UI Tools for Unreal MCP.

This module provides tools for creating UI dialogs in Unreal Engine.
"""

import logging
from typing import Dict, List, Any, Optional
from mcp.server.fastmcp import FastMCP, Context

# Get logger
logger = logging.getLogger("UnrealMCP")

def register_ui_tools(mcp: FastMCP):
    """Register UI tools with the MCP server."""
    
    @mcp.tool()
    def show_function_generation_dialog(
        ctx: Context,
        blueprint_name: str = None
    ) -> Dict[str, Any]:
        """
        Show a dialog for generating Blueprint functions.
        
        Args:
            blueprint_name: Optional name of the target Blueprint
            
        Returns:
            Dict containing the dialog result
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {}
            if blueprint_name:
                params["blueprint_name"] = blueprint_name
                
            response = unreal.send_command("show_function_generation_dialog", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Show function generation dialog response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error showing function generation dialog: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    @mcp.tool()
    def show_ai_configuration_dialog(
        ctx: Context
    ) -> Dict[str, Any]:
        """
        Show a dialog for configuring AI services.
        
        Returns:
            Dict containing the dialog result
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
                
            response = unreal.send_command("show_ai_configuration_dialog", {})
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Show AI configuration dialog response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error showing AI configuration dialog: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    logger.info("UI tools registered successfully")
