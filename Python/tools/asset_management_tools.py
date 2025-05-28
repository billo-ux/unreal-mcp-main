"""
Asset Management Tools for Unreal MCP.

This module provides tools for importing, exporting, renaming, and deleting assets in the Content Browser.
"""

import logging
from typing import Dict, List, Any, Optional
from mcp.server.fastmcp import FastMCP, Context
from unreal_mcp_server import get_unreal_connection

logger = logging.getLogger("UnrealMCP")

def register_asset_management_tools(mcp: FastMCP):
    """Register asset management tools with the MCP server."""
    # ... (tools will be added here in subsequent steps)

    @mcp.tool()
    def import_asset(ctx: Context, source_file: str, destination_path: str, asset_name: str) -> Dict[str, Any]:
        """
        Import an asset into the Content Browser.
        Args:
            source_file: Path to the source file (e.g., FBX, PNG)
            destination_path: Path in the Content Browser (e.g., /Game/Imported)
            asset_name: Name for the imported asset
        Returns:
            Dict with success status and asset path
        """
        try:
            params = {"source_file": source_file, "destination_path": destination_path, "asset_name": asset_name}
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            response = unreal.send_command("import_asset", params)
            return response or {"success": False, "message": "No response from Unreal Engine"}
        except Exception as e:
            logger.error(f"Error importing asset: {e}")
            return {"success": False, "message": str(e)}

    @mcp.tool()
    def export_asset(ctx: Context, asset_path: str, export_path: str) -> Dict[str, Any]:
        """
        Export an asset from the Content Browser.
        Args:
            asset_path: Path to the asset in the Content Browser (e.g., /Game/Imported/MyAsset)
            export_path: Destination path on disk
        Returns:
            Dict with success status and export path
        """
        try:
            params = {"asset_path": asset_path, "export_path": export_path}
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            response = unreal.send_command("export_asset", params)
            return response or {"success": False, "message": "No response from Unreal Engine"}
        except Exception as e:
            logger.error(f"Error exporting asset: {e}")
            return {"success": False, "message": str(e)}

    @mcp.tool()
    def list_assets(ctx: Context, content_path: str = "/Game") -> Dict[str, Any]:
        """
        List all assets in a given Content Browser path.
        Args:
            content_path: Path in the Content Browser (default: /Game)
        Returns:
            Dict with asset names and paths
        """
        try:
            params = {"content_path": content_path}
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            response = unreal.send_command("list_assets", params)
            return response or {"success": False, "message": "No response from Unreal Engine"}
        except Exception as e:
            logger.error(f"Error listing assets: {e}")
            return {"success": False, "message": str(e)} 