"""
Basic Asset Tools for Unreal MCP.

This module provides tools for creating, duplicating, renaming, and deleting basic Unreal Engine assets: Blueprints, Levels, Materials, Niagara Systems, Static Meshes, etc.
"""

import logging
from typing import Dict, List, Any, Optional
from mcp.server.fastmcp import FastMCP, Context

logger = logging.getLogger("UnrealMCP")

def register_basic_asset_tools(mcp: FastMCP):
    """Register basic asset tools with the MCP server."""
    from unreal_mcp_server import get_unreal_connection

    @mcp.tool()
    def create_blueprint(
        ctx: Context,
        name: str,
        parent_class: str = "/Script/Engine.Actor",
        save_path: str = "/Game/Blueprints"
    ) -> Dict[str, Any]:
        """
        Create a new Blueprint asset.
        Args:
            name: Name of the Blueprint
            parent_class: Parent class (default: Actor)
            save_path: Path to save the Blueprint
        Returns:
            Dict with success status and asset path
        """
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            params = {"name": name, "parent_class": parent_class, "save_path": save_path}
            response = unreal.send_command("create_blueprint_class", params)
            if not response or response.get("status") != "success":
                logger.error(f"Failed to create Blueprint: {response}")
                return {"success": False, "message": f"Failed to create Blueprint: {response.get('error', 'Unknown error')}"}
            asset_path = response.get("result", {}).get("asset_path", "")
            return {"success": True, "message": f"Successfully created Blueprint: {asset_path}", "asset_path": asset_path}
        except Exception as e:
            logger.error(f"Error creating Blueprint: {e}")
            return {"success": False, "message": str(e)}

    @mcp.tool()
    def create_level(
        ctx: Context,
        name: str,
        template_level: str = None,
        save_path: str = "/Game/Maps"
    ) -> Dict[str, Any]:
        """
        Create a new Level asset.
        Args:
            name: Name of the Level
            template_level: Optional template to base the level on
            save_path: Path to save the Level
        Returns:
            Dict with success status and asset path
        """
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            params = {"asset_name": name, "save_path": save_path}
            if template_level:
                params["template_level"] = template_level
            response = unreal.send_command("create_level", params)
            if not response or response.get("status") != "success":
                logger.error(f"Failed to create Level: {response}")
                return {"success": False, "message": f"Failed to create Level: {response.get('error', 'Unknown error')}"}
            asset_path = response.get("result", {}).get("asset_path", "")
            return {"success": True, "message": f"Successfully created Level: {asset_path}", "asset_path": asset_path}
        except Exception as e:
            logger.error(f"Error creating Level: {e}")
            return {"success": False, "message": str(e)}

    @mcp.tool()
    def create_material(
        ctx: Context,
        name: str,
        save_path: str = "/Game/Materials"
    ) -> Dict[str, Any]:
        """
        Create a new Material asset.
        Args:
            name: Name of the Material
            save_path: Path to save the Material
        Returns:
            Dict with success status and asset path
        """
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            params = {"asset_name": name, "save_path": save_path}
            response = unreal.send_command("create_material", params)
            if not response or response.get("status") != "success":
                logger.error(f"Failed to create Material: {response}")
                return {"success": False, "message": f"Failed to create Material: {response.get('error', 'Unknown error')}"}
            asset_path = response.get("result", {}).get("asset_path", "")
            return {"success": True, "message": f"Successfully created Material: {asset_path}", "asset_path": asset_path}
        except Exception as e:
            logger.error(f"Error creating Material: {e}")
            return {"success": False, "message": str(e)}

    @mcp.tool()
    def create_niagara_system(
        ctx: Context,
        name: str,
        save_path: str = "/Game/Effects"
    ) -> Dict[str, Any]:
        """
        Create a new Niagara System asset.
        Args:
            name: Name of the Niagara System
            save_path: Path to save the Niagara System
        Returns:
            Dict with success status and asset path
        """
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            params = {"asset_name": name, "save_path": save_path}
            response = unreal.send_command("create_niagara_system", params)
            if not response or response.get("status") != "success":
                logger.error(f"Failed to create Niagara System: {response}")
                return {"success": False, "message": f"Failed to create Niagara System: {response.get('error', 'Unknown error')}"}
            asset_path = response.get("result", {}).get("asset_path", "")
            return {"success": True, "message": f"Successfully created Niagara System: {asset_path}", "asset_path": asset_path}
        except Exception as e:
            logger.error(f"Error creating Niagara System: {e}")
            return {"success": False, "message": str(e)}

    @mcp.tool()
    def create_static_mesh(
        ctx: Context,
        name: str,
        source_file: str,
        save_path: str = "/Game/Meshes"
    ) -> Dict[str, Any]:
        """
        Import a new Static Mesh asset from a source file.
        Args:
            name: Name of the Static Mesh
            source_file: Path to the source mesh file (FBX, OBJ, etc.)
            save_path: Path to save the Static Mesh
        Returns:
            Dict with success status and asset path
        """
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            params = {"asset_name": name, "source_file": source_file, "save_path": save_path}
            response = unreal.send_command("import_static_mesh", params)
            if not response or response.get("status") != "success":
                logger.error(f"Failed to import Static Mesh: {response}")
                return {"success": False, "message": f"Failed to import Static Mesh: {response.get('error', 'Unknown error')}"}
            asset_path = response.get("result", {}).get("asset_path", "")
            return {"success": True, "message": f"Successfully imported Static Mesh: {asset_path}", "asset_path": asset_path}
        except Exception as e:
            logger.error(f"Error importing Static Mesh: {e}")
            return {"success": False, "message": str(e)}

    @mcp.tool()
    def duplicate_asset(ctx: Context, asset_path: str, new_name: str, save_path: str = None) -> Dict[str, str]:
        """
        Duplicate an asset (Blueprint, Material, Niagara System, Static Mesh, etc.).
        Args:
            asset_path: Path to the asset to duplicate (e.g., /Game/Blueprints/MyBP)
            new_name: Name for the duplicated asset
            save_path: Path to save the duplicated asset (default: same as original)
        Returns:
            Dict with success status and new asset path
        Example:
            duplicate_asset(ctx, '/Game/Blueprints/MyBP', 'MyBP_Copy', '/Game/Blueprints')
        """
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            params = {"asset_path": asset_path, "new_name": new_name}
            if save_path:
                params["save_path"] = save_path
            response = unreal.send_command("duplicate_asset", params)
            if not response or response.get("status") != "success":
                logger.error(f"Failed to duplicate asset: {response}")
                return {"success": False, "message": f"Failed to duplicate asset: {response.get('error', 'Unknown error')}"}
            new_asset_path = response.get("result", {}).get("asset_path", "")
            return {"success": True, "message": f"Successfully duplicated asset: {new_asset_path}", "asset_path": new_asset_path}
        except Exception as e:
            logger.error(f"Error duplicating asset: {e}")
            return {"success": False, "message": str(e)}

    @mcp.tool()
    def rename_asset(ctx: Context, asset_path: str, new_name: str) -> Dict[str, str]:
        """
        Rename an asset (Blueprint, Material, Niagara System, Static Mesh, etc.).
        Args:
            asset_path: Path to the asset to rename (e.g., /Game/Blueprints/MyBP)
            new_name: New name for the asset
        Returns:
            Dict with success status and new asset path
        Example:
            rename_asset(ctx, '/Game/Blueprints/MyBP', 'MyRenamedBP')
        """
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            params = {"asset_path": asset_path, "new_name": new_name}
            response = unreal.send_command("rename_asset", params)
            if not response or response.get("status") != "success":
                logger.error(f"Failed to rename asset: {response}")
                return {"success": False, "message": f"Failed to rename asset: {response.get('error', 'Unknown error')}"}
            new_asset_path = response.get("result", {}).get("asset_path", "")
            return {"success": True, "message": f"Successfully renamed asset: {new_asset_path}", "asset_path": new_asset_path}
        except Exception as e:
            logger.error(f"Error renaming asset: {e}")
            return {"success": False, "message": str(e)}

    @mcp.tool()
    def delete_asset(ctx: Context, asset_path: str) -> Dict[str, str]:
        """
        Delete an asset (Blueprint, Material, Niagara System, Static Mesh, etc.).
        Args:
            asset_path: Path to the asset to delete (e.g., /Game/Blueprints/MyBP)
        Returns:
            Dict with success status
        Example:
            delete_asset(ctx, '/Game/Blueprints/MyBP')
        """
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            params = {"asset_path": asset_path}
            response = unreal.send_command("delete_asset", params)
            if not response or response.get("status") != "success":
                logger.error(f"Failed to delete asset: {response}")
                return {"success": False, "message": f"Failed to delete asset: {response.get('error', 'Unknown error')}"}
            return {"success": True, "message": f"Successfully deleted asset: {asset_path}"}
        except Exception as e:
            logger.error(f"Error deleting asset: {e}")
            return {"success": False, "message": str(e)} 