"""
Asset Management Tools for Unreal MCP.

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

def register_asset_management_tools(mcp: FastMCP):
    """Register asset management tools with the MCP server."""
    # ... (tools will be added here in subsequent steps)

    @mcp.tool()
    def import_asset(ctx: Context, source_file: str, destination_path: str, asset_name: str) -> Dict[str, str]:
        """
        Import an asset into the Content Browser.
        Args:
            source_file: Path to the source file (e.g., FBX, PNG)
            destination_path: Path in the Content Browser (e.g., /Game/Imported)
            asset_name: Name for the imported asset
        Returns:
            Dict with success status and asset path
        Example:
            import_asset(ctx, source_file="/tmp/mesh.fbx", destination_path="/Game/Imported", asset_name="MyMesh")
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
    def export_asset(ctx: Context, asset_path: str, export_path: str) -> Dict[str, str]:
        """
        Export an asset from the Content Browser.
        Args:
            asset_path: Path to the asset in the Content Browser (e.g., /Game/Imported/MyAsset)
            export_path: Destination path on disk
        Returns:
            Dict with success status and export path
        Example:
            export_asset(ctx, asset_path="/Game/Imported/MyMesh", export_path="/tmp/exported_mesh.fbx")
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
    def list_assets(ctx: Context, content_path: str = "/Game", with_metadata: bool = False) -> Dict[str, object]:
        """
        List all assets in a given Content Browser path, optionally including metadata for each asset.
        Args:
            content_path: Path in the Content Browser (default: /Game)
            with_metadata: If True, include metadata (type, class, tags, etc.) for each asset
        Returns:
            Dict with asset names and paths, and optionally metadata
        Example:
            list_assets(ctx, content_path="/Game", with_metadata=True)
        """
        try:
            params = {"content_path": content_path, "with_metadata": with_metadata}
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            response = unreal.send_command("list_assets", params)
            return response or {"success": False, "message": "No response from Unreal Engine"}
        except Exception as e:
            logger.error(f"Error listing assets: {e}")
            return {"success": False, "message": str(e)}

    @mcp.tool()
    def get_asset_metadata(ctx: Context, asset_path: str) -> Dict[str, object]:
        """
        Fetch detailed metadata for a single asset.
        Args:
            asset_path: Path to the asset (e.g., /Game/Blueprints/BP_MyActor)
        Returns:
            Dict with metadata fields (type, class, tags, size, references, etc.)
        Example:
            get_asset_metadata(ctx, asset_path="/Game/Blueprints/BP_MyActor")
        """
        try:
            params = {"asset_path": asset_path}
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            response = unreal.send_command("get_asset_metadata", params)
            return response or {"success": False, "message": "No response from Unreal Engine"}
        except Exception as e:
            logger.error(f"Error fetching asset metadata: {e}")
            return {"success": False, "message": str(e)}

    @mcp.tool()
    def extract_asset_examples(ctx: Context, asset_type: str, count: int = 3) -> Dict[str, object]:
        """
        Extract real asset/code/Blueprint/script examples for a given asset type.
        Args:
            asset_type: The type of asset to extract examples for (e.g., 'Blueprint', 'Material', 'WidgetBlueprint', 'Level')
            count: Number of examples to return (default: 3)
        Returns:
            Dict with a list of example dicts, each containing asset path, name, and optionally code/blueprint/script snippet
        Example:
            extract_asset_examples(ctx, asset_type="Blueprint", count=2)
        """
        try:
            params = {"asset_type": asset_type, "count": count}
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine", "examples": []}
            response = unreal.send_command("extract_asset_examples", params)
            return response or {"success": False, "message": "No response from Unreal Engine", "examples": []}
        except Exception as e:
            logger.error(f"Error extracting asset examples: {e}")
            return {"success": False, "message": str(e), "examples": []}

    @mcp.tool()
    def find_asset_references(ctx: Context, asset_path: str) -> Dict[str, object]:
        """
        Find all references to a given asset in the project.
        Args:
            asset_path: Path to the asset (e.g., /Game/Materials/M_MyMaterial)
        Returns:
            Dict with success status and a list of referencing assets/actors
        Example:
            find_asset_references(ctx, asset_path="/Game/Materials/M_MyMaterial")
        """
        from unreal_mcp_server import get_unreal_connection
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "references": [], "message": "Failed to connect to Unreal Engine"}
            response = unreal.send_command("find_asset_references", {"asset_path": asset_path})
            if not response or response.get("status") != "success":
                logger.error(f"Failed to find references: {response}")
                return {"success": False, "references": [], "message": response.get("error", "Unknown error") if response else "No response from Unreal Engine"}
            references = response.get("result", {}).get("references", [])
            return {"success": True, "references": references}
        except Exception as e:
            logger.error(f"Error finding asset references: {e}")
            return {"success": False, "references": [], "message": str(e)} 