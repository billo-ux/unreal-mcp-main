"""
Project Tools for Unreal MCP.

This module provides tools for managing project-wide settings and configuration.
"""

import logging
from typing import Dict, Any, List
from mcp.server.fastmcp import FastMCP, Context

# Get logger
logger = logging.getLogger("UnrealMCP")

def register_project_tools(mcp: FastMCP):
    """Register project tools with the MCP server."""
    
    @mcp.tool()
    def create_input_mapping(
        ctx: Context,
        action_name: str,
        key: str,
        input_type: str = "Action"
    ) -> Dict[str, Any]:
        """
        Create an input mapping for the project.
        
        Args:
            action_name: Name of the input action
            key: Key to bind (SpaceBar, LeftMouseButton, etc.)
            input_type: Type of input mapping (Action or Axis)
            
        Returns:
            Response indicating success or failure
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {
                "action_name": action_name,
                "key": key,
                "input_type": input_type
            }
            
            logger.info(f"Creating input mapping '{action_name}' with key '{key}'")
            response = unreal.send_command("create_input_mapping", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Input mapping creation response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error creating input mapping: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    @mcp.tool()
    def get_project_setting(ctx: Context, setting_name: str) -> Dict[str, Any]:
        """
        Get a project setting by name.
        Args:
            setting_name: Name of the project setting (e.g., 'DefaultGameMode')
        Returns:
            Dict with the setting value
        """
        from unreal_mcp_server import get_unreal_connection
        try:
            params = {"setting_name": setting_name}
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            response = unreal.send_command("get_project_setting", params)
            return response or {"success": False, "message": "No response from Unreal Engine"}
        except Exception as e:
            logger.error(f"Error getting project setting: {e}")
            return {"success": False, "message": str(e)}

    @mcp.tool()
    def set_project_setting(ctx: Context, setting_name: str, value) -> Dict[str, Any]:
        """
        Set a project setting by name.
        Args:
            setting_name: Name of the project setting
            value: Value to set
        Returns:
            Dict with success status
        """
        from unreal_mcp_server import get_unreal_connection
        try:
            params = {"setting_name": setting_name, "value": value}
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            response = unreal.send_command("set_project_setting", params)
            return response or {"success": False, "message": "No response from Unreal Engine"}
        except Exception as e:
            logger.error(f"Error setting project setting: {e}")
            return {"success": False, "message": str(e)}

    @mcp.tool()
    def list_plugins(ctx: Context) -> Dict[str, Any]:
        """
        List all plugins in the project.
        Returns:
            Dict with plugin names and statuses
        """
        from unreal_mcp_server import get_unreal_connection
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            response = unreal.send_command("list_plugins", {})
            return response or {"success": False, "message": "No response from Unreal Engine"}
        except Exception as e:
            logger.error(f"Error listing plugins: {e}")
            return {"success": False, "message": str(e)}

    @mcp.tool()
    def enable_plugin(ctx: Context, plugin_name: str) -> Dict[str, Any]:
        """
        Enable a plugin by name.
        Args:
            plugin_name: Name of the plugin to enable
        Returns:
            Dict with success status
        """
        from unreal_mcp_server import get_unreal_connection
        try:
            params = {"plugin_name": plugin_name}
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            response = unreal.send_command("enable_plugin", params)
            return response or {"success": False, "message": "No response from Unreal Engine"}
        except Exception as e:
            logger.error(f"Error enabling plugin: {e}")
            return {"success": False, "message": str(e)}

    @mcp.tool()
    def disable_plugin(ctx: Context, plugin_name: str) -> Dict[str, Any]:
        """
        Disable a plugin by name.
        Args:
            plugin_name: Name of the plugin to disable
        Returns:
            Dict with success status
        """
        from unreal_mcp_server import get_unreal_connection
        try:
            params = {"plugin_name": plugin_name}
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            response = unreal.send_command("disable_plugin", params)
            return response or {"success": False, "message": "No response from Unreal Engine"}
        except Exception as e:
            logger.error(f"Error disabling plugin: {e}")
            return {"success": False, "message": str(e)}
    
    @mcp.tool()
    def build_project(ctx: Context, configuration: str = "Development") -> Dict[str, Any]:
        """
        Build the Unreal project.
        Args:
            configuration: Build configuration (Development, Shipping, etc.)
        Returns:
            Dict with success status and build output
        Example:
            build_project(ctx, configuration="Shipping")
        TODO:
            Implement project build logic.
        """
        # TODO: Implement project build
        return {"success": False, "message": "Not yet implemented"}

    @mcp.tool()
    def cook_project(ctx: Context, platforms: List[str]) -> Dict[str, Any]:
        """
        Cook the Unreal project for specified platforms.
        Args:
            platforms: List of platform names (e.g., ["Windows", "Linux"])
        Returns:
            Dict with success status and cook output
        Example:
            cook_project(ctx, platforms=["Windows"])
        TODO:
            Implement project cook logic.
        """
        # TODO: Implement project cook
        return {"success": False, "message": "Not yet implemented"}

    @mcp.tool()
    def package_project(ctx: Context, platform: str, output_path: str) -> Dict[str, Any]:
        """
        Package the Unreal project for a specific platform.
        Args:
            platform: Platform name (e.g., "Windows")
            output_path: Path to output the packaged build
        Returns:
            Dict with success status and package output
        Example:
            package_project(ctx, platform="Windows", output_path="/Builds/Windows")
        TODO:
            Implement project packaging logic.
        """
        # TODO: Implement project packaging
        return {"success": False, "message": "Not yet implemented"}

    @mcp.tool()
    def run_source_control_command(ctx: Context, command: str, args: Dict[str, str] = None) -> Dict[str, Any]:
        """
        Run a source control command (Git, Perforce, etc.).
        Args:
            command: Source control command (e.g., "status", "commit")
            args: Arguments for the command
        Returns:
            Dict with success status and command output
        Example:
            run_source_control_command(ctx, command="status")
        TODO:
            Implement source control integration.
        """
        # TODO: Implement source control integration
        return {"success": False, "message": "Not yet implemented"}

    @mcp.tool()
    def manage_localization_asset(ctx: Context, action: str, asset_path: str, locale: str = None) -> Dict[str, Any]:
        """
        Manage localization assets (import/export/list).
        Args:
            action: Action to perform (import, export, list)
            asset_path: Path to the localization asset
            locale: Locale code (optional)
        Returns:
            Dict with success status and action output
        Example:
            manage_localization_asset(ctx, action="list", asset_path="/Game/Localization")
        TODO:
            Implement localization asset management.
        """
        # TODO: Implement localization asset management
        return {"success": False, "message": "Not yet implemented"}

    @mcp.tool()
    def run_automation_test(ctx: Context, test_name: str) -> Dict[str, Any]:
        """
        Run an automation test by name.
        Args:
            test_name: Name of the test to run
        Returns:
            Dict with success status and test results
        Example:
            run_automation_test(ctx, test_name="MyTest")
        TODO:
            Implement automation test running.
        """
        # TODO: Implement automation test running
        return {"success": False, "message": "Not yet implemented"}

    @mcp.tool()
    def report_automation_test_results(ctx: Context, test_name: str) -> Dict[str, Any]:
        """
        Report results for a given automation test.
        Args:
            test_name: Name of the test
        Returns:
            Dict with test result details
        Example:
            report_automation_test_results(ctx, test_name="MyTest")
        TODO:
            Implement automation test result reporting.
        """
        # TODO: Implement automation test result reporting
        return {"success": False, "message": "Not yet implemented"}

    logger.info("Project tools registered successfully") 