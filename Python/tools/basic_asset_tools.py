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

    @mcp.tool()
    def create_material_instance(ctx: Context, name: str, parent_material: str, save_path: str = "/Game/Materials") -> Dict[str, Any]:
        """
        Create a new Material Instance asset.
        Args:
            name: Name of the Material Instance
            parent_material: Path to the parent Material asset
            save_path: Path to save the Material Instance
        Returns:
            Dict with success status and asset path
        Example:
            create_material_instance(ctx, "MI_MyMaterial", "/Game/Materials/M_Master")
        """
        try:
            params = {"asset_name": name, "parent_material": parent_material, "save_path": save_path}
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            response = unreal.send_command("create_material_instance", params)
            if not response or response.get("status") != "success":
                logger.error(f"Failed to create Material Instance: {response}")
                return {"success": False, "message": f"Failed to create Material Instance: {response.get('error', 'Unknown error')}"}
            asset_path = response.get("result", {}).get("asset_path", "")
            return {"success": True, "message": f"Successfully created Material Instance: {asset_path}", "asset_path": asset_path}
        except Exception as e:
            logger.error(f"Error creating Material Instance: {e}")
            return {"success": False, "message": str(e)}

    @mcp.tool()
    def create_niagara_emitter(ctx: Context, name: str, save_path: str = "/Game/Effects") -> Dict[str, Any]:
        """
        Create a new Niagara Emitter asset.
        Args:
            name: Name of the Niagara Emitter
            save_path: Path to save the Niagara Emitter
        Returns:
            Dict with success status and asset path
        Example:
            create_niagara_emitter(ctx, "MyEmitter")
        """
        try:
            params = {"asset_name": name, "save_path": save_path}
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            response = unreal.send_command("create_niagara_emitter", params)
            if not response or response.get("status") != "success":
                logger.error(f"Failed to create Niagara Emitter: {response}")
                return {"success": False, "message": f"Failed to create Niagara Emitter: {response.get('error', 'Unknown error')}"}
            asset_path = response.get("result", {}).get("asset_path", "")
            return {"success": True, "message": f"Successfully created Niagara Emitter: {asset_path}", "asset_path": asset_path}
        except Exception as e:
            logger.error(f"Error creating Niagara Emitter: {e}")
            return {"success": False, "message": str(e)}

    @mcp.tool()
    def create_texture(ctx: Context, name: str, source_file: str, save_path: str = "/Game/Textures") -> Dict[str, Any]:
        """
        Import a new Texture asset from a source file.
        Args:
            name: Name of the Texture
            source_file: Path to the source image file (PNG, JPG, etc.)
            save_path: Path to save the Texture
        Returns:
            Dict with success status and asset path
        """
        try:
            params = {"asset_name": name, "source_file": source_file, "save_path": save_path}
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            response = unreal.send_command("import_texture", params)
            if not response or response.get("status") != "success":
                logger.error(f"Failed to import Texture: {response}")
                return {"success": False, "message": f"Failed to import Texture: {response.get('error', 'Unknown error')}"}
            asset_path = response.get("result", {}).get("asset_path", "")
            return {"success": True, "message": f"Successfully imported Texture: {asset_path}", "asset_path": asset_path}
        except Exception as e:
            logger.error(f"Error importing Texture: {e}")
            return {"success": False, "message": str(e)}

    @mcp.tool()
    def create_sound_cue(ctx: Context, name: str, save_path: str = "/Game/Audio") -> Dict[str, Any]:
        """
        Create a new Sound Cue asset.
        Args:
            name: Name of the Sound Cue
            save_path: Path to save the Sound Cue
        Returns:
            Dict with success status and asset path
        Example:
            create_sound_cue(ctx, "MySoundCue")
        """
        try:
            params = {"asset_name": name, "save_path": save_path}
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            response = unreal.send_command("create_sound_cue", params)
            if not response or response.get("status") != "success":
                logger.error(f"Failed to create Sound Cue: {response}")
                return {"success": False, "message": f"Failed to create Sound Cue: {response.get('error', 'Unknown error')}"}
            asset_path = response.get("result", {}).get("asset_path", "")
            return {"success": True, "message": f"Successfully created Sound Cue: {asset_path}", "asset_path": asset_path}
        except Exception as e:
            logger.error(f"Error creating Sound Cue: {e}")
            return {"success": False, "message": str(e)}

    @mcp.tool()
    def create_sound_wave(ctx: Context, name: str, source_file: str, save_path: str = "/Game/Audio") -> Dict[str, Any]:
        """
        Import a new Sound Wave asset from a source file.
        Args:
            name: Name of the Sound Wave
            source_file: Path to the source audio file (WAV, etc.)
            save_path: Path to save the Sound Wave
        Returns:
            Dict with success status and asset path
        Example:
            create_sound_wave(ctx, "MySound", "/path/to/sound.wav")
        """
        try:
            params = {"asset_name": name, "source_file": source_file, "save_path": save_path}
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            response = unreal.send_command("import_sound_wave", params)
            if not response or response.get("status") != "success":
                logger.error(f"Failed to import Sound Wave: {response}")
                return {"success": False, "message": f"Failed to import Sound Wave: {response.get('error', 'Unknown error')}"}
            asset_path = response.get("result", {}).get("asset_path", "")
            return {"success": True, "message": f"Successfully imported Sound Wave: {asset_path}", "asset_path": asset_path}
        except Exception as e:
            logger.error(f"Error importing Sound Wave: {e}")
            return {"success": False, "message": str(e)}

    @mcp.tool()
    def create_font(ctx: Context, name: str, source_file: str, save_path: str = "/Game/Fonts") -> Dict[str, Any]:
        """
        Import a new Font asset from a source file.
        Args:
            name: Name of the Font
            source_file: Path to the source font file (TTF, OTF, etc.)
            save_path: Path to save the Font
        Returns:
            Dict with success status and asset path
        Example:
            create_font(ctx, "MyFont", "/path/to/font.ttf")
        """
        try:
            params = {"asset_name": name, "source_file": source_file, "save_path": save_path}
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            response = unreal.send_command("import_font", params)
            if not response or response.get("status") != "success":
                logger.error(f"Failed to import Font: {response}")
                return {"success": False, "message": f"Failed to import Font: {response.get('error', 'Unknown error')}"}
            asset_path = response.get("result", {}).get("asset_path", "")
            return {"success": True, "message": f"Successfully imported Font: {asset_path}", "asset_path": asset_path}
        except Exception as e:
            logger.error(f"Error importing Font: {e}")
            return {"success": False, "message": str(e)}

    @mcp.tool()
    def create_curve(ctx: Context, name: str, curve_type: str = "FloatCurve", save_path: str = "/Game/Curves") -> Dict[str, Any]:
        """
        Create a new Curve asset.
        Args:
            name: Name of the Curve
            curve_type: Type of curve (FloatCurve, VectorCurve, etc.)
            save_path: Path to save the Curve
        Returns:
            Dict with success status and asset path
        Example:
            create_curve(ctx, "MyCurve", "FloatCurve")
        """
        try:
            params = {"asset_name": name, "curve_type": curve_type, "save_path": save_path}
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            response = unreal.send_command("create_curve", params)
            if not response or response.get("status") != "success":
                logger.error(f"Failed to create Curve: {response}")
                return {"success": False, "message": f"Failed to create Curve: {response.get('error', 'Unknown error')}"}
            asset_path = response.get("result", {}).get("asset_path", "")
            return {"success": True, "message": f"Successfully created Curve: {asset_path}", "asset_path": asset_path}
        except Exception as e:
            logger.error(f"Error creating Curve: {e}")
            return {"success": False, "message": str(e)}

    @mcp.tool()
    def create_data_table(ctx: Context, name: str, row_struct: str, save_path: str = "/Game/Data") -> Dict[str, Any]:
        """
        Create a new Data Table asset.
        Args:
            name: Name of the Data Table
            row_struct: Name of the row struct to use
            save_path: Path to save the Data Table
        Returns:
            Dict with success status and asset path
        Example:
            create_data_table(ctx, "MyDataTable", "MyRowStruct")
        """
        try:
            params = {"asset_name": name, "row_struct": row_struct, "save_path": save_path}
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            response = unreal.send_command("create_data_table", params)
            if not response or response.get("status") != "success":
                logger.error(f"Failed to create Data Table: {response}")
                return {"success": False, "message": f"Failed to create Data Table: {response.get('error', 'Unknown error')}"}
            asset_path = response.get("result", {}).get("asset_path", "")
            return {"success": True, "message": f"Successfully created Data Table: {asset_path}", "asset_path": asset_path}
        except Exception as e:
            logger.error(f"Error creating Data Table: {e}")
            return {"success": False, "message": str(e)}

    @mcp.tool()
    def create_struct(ctx: Context, name: str, fields: Dict[str, str], save_path: str = "/Game/Data") -> Dict[str, Any]:
        """
        Create a new Struct asset.
        Args:
            name: Name of the Struct
            fields: Dictionary of field names and types
            save_path: Path to save the Struct
        Returns:
            Dict with success status and asset path
        Note:
            Unreal may require additional setup for struct fields after creation.
        Example:
            create_struct(ctx, "MyStruct", {"Health": "float", "Name": "FString"})
        """
        try:
            params = {"asset_name": name, "fields": fields, "save_path": save_path}
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            response = unreal.send_command("create_struct", params)
            if not response or response.get("status") != "success":
                logger.error(f"Failed to create Struct: {response}")
                return {"success": False, "message": f"Failed to create Struct: {response.get('error', 'Unknown error')}"}
            asset_path = response.get("result", {}).get("asset_path", "")
            return {"success": True, "message": f"Successfully created Struct: {asset_path}", "asset_path": asset_path}
        except Exception as e:
            logger.error(f"Error creating Struct: {e}")
            return {"success": False, "message": str(e)}

    @mcp.tool()
    def create_enum(ctx: Context, name: str, entries: List[str], save_path: str = "/Game/Data") -> Dict[str, Any]:
        """
        Create a new Enum asset.
        Args:
            name: Name of the Enum
            entries: List of enum entry names
            save_path: Path to save the Enum
        Returns:
            Dict with success status and asset path
        Note:
            Unreal may require additional setup for enum entries after creation.
        Example:
            create_enum(ctx, "MyEnum", ["Idle", "Running", "Jumping"])
        """
        try:
            params = {"asset_name": name, "entries": entries, "save_path": save_path}
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            response = unreal.send_command("create_enum", params)
            if not response or response.get("status") != "success":
                logger.error(f"Failed to create Enum: {response}")
                return {"success": False, "message": f"Failed to create Enum: {response.get('error', 'Unknown error')}"}
            asset_path = response.get("result", {}).get("asset_path", "")
            return {"success": True, "message": f"Successfully created Enum: {asset_path}", "asset_path": asset_path}
        except Exception as e:
            logger.error(f"Error creating Enum: {e}")
            return {"success": False, "message": str(e)}

    @mcp.tool()
    def create_slate_brush(ctx: Context, name: str, texture_path: str, save_path: str = "/Game/UI") -> Dict[str, Any]:
        """
        Create a new Slate Brush asset.
        Args:
            name: Name of the Slate Brush
            texture_path: Path to the texture asset
            save_path: Path to save the Slate Brush
        Returns:
            Dict with success status and asset path
        Note:
            Unreal may require additional setup for brush properties after creation.
        Example:
            create_slate_brush(ctx, "MyBrush", "/Game/Textures/T_Brush")
        """
        try:
            params = {"asset_name": name, "texture_path": texture_path, "save_path": save_path}
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            response = unreal.send_command("create_slate_brush", params)
            if not response or response.get("status") != "success":
                logger.error(f"Failed to create Slate Brush: {response}")
                return {"success": False, "message": f"Failed to create Slate Brush: {response.get('error', 'Unknown error')}"}
            asset_path = response.get("result", {}).get("asset_path", "")
            return {"success": True, "message": f"Successfully created Slate Brush: {asset_path}", "asset_path": asset_path}
        except Exception as e:
            logger.error(f"Error creating Slate Brush: {e}")
            return {"success": False, "message": str(e)}

    @mcp.tool()
    def create_paper2d_sprite(ctx: Context, name: str, texture_path: str, save_path: str = "/Game/Sprites") -> Dict[str, Any]:
        """
        Create a new Paper2D Sprite asset.
        Args:
            name: Name of the Sprite
            texture_path: Path to the texture asset
            save_path: Path to save the Sprite
        Returns:
            Dict with success status and asset path
        Note:
            Unreal may require additional setup for sprite properties after creation.
        Example:
            create_paper2d_sprite(ctx, "MySprite", "/Game/Textures/T_Sprite")
        """
        try:
            params = {"asset_name": name, "texture_path": texture_path, "save_path": save_path}
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            response = unreal.send_command("create_paper2d_sprite", params)
            if not response or response.get("status") != "success":
                logger.error(f"Failed to create Paper2D Sprite: {response}")
                return {"success": False, "message": f"Failed to create Paper2D Sprite: {response.get('error', 'Unknown error')}"}
            asset_path = response.get("result", {}).get("asset_path", "")
            return {"success": True, "message": f"Successfully created Paper2D Sprite: {asset_path}", "asset_path": asset_path}
        except Exception as e:
            logger.error(f"Error creating Paper2D Sprite: {e}")
            return {"success": False, "message": str(e)}

    @mcp.tool()
    def create_paper2d_tile_map(ctx: Context, name: str, width: int, height: int, tile_set: str, save_path: str = "/Game/TileMaps") -> Dict[str, Any]:
        """
        Create a new Paper2D Tile Map asset.
        Args:
            name: Name of the Tile Map
            width: Width of the tile map (in tiles)
            height: Height of the tile map (in tiles)
            tile_set: Path to the tile set asset
            save_path: Path to save the Tile Map
        Returns:
            Dict with success status and asset path
        Note:
            This is a high-complexity asset and may require additional setup in Unreal Editor after creation.
        Example:
            create_paper2d_tile_map(ctx, "MyTileMap", 10, 10, "/Game/TileSets/T_TileSet")
        """
        try:
            params = {"asset_name": name, "width": width, "height": height, "tile_set": tile_set, "save_path": save_path}
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            response = unreal.send_command("create_paper2d_tile_map", params)
            if not response or response.get("status") != "success":
                logger.error(f"Failed to create Paper2D Tile Map: {response}")
                return {"success": False, "message": f"Failed to create Paper2D Tile Map: {response.get('error', 'Unknown error')}"}
            asset_path = response.get("result", {}).get("asset_path", "")
            return {"success": True, "message": f"Successfully created Paper2D Tile Map: {asset_path}", "asset_path": asset_path}
        except Exception as e:
            logger.error(f"Error creating Paper2D Tile Map: {e}")
            return {"success": False, "message": str(e)}

    @mcp.tool()
    def batch_create_assets(ctx: Context, assets: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Batch create basic assets.
        Args:
            assets: List of dicts with keys 'type', 'name', and 'save_path'. Example:
                [{"type": "Blueprint", "name": "BP_MyActor", "save_path": "/Game/Blueprints"}, ...]
        Returns:
            Dict with success status and a list of results for each asset.
        Example:
            batch_create_assets(ctx, [{"type": "Blueprint", "name": "BP_MyActor", "save_path": "/Game/Blueprints"}])
        """
        from unreal_mcp_server import get_unreal_connection
        results = []
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine", "results": []}
            for asset in assets:
                asset_type = asset.get("type")
                name = asset.get("name")
                save_path = asset.get("save_path")
                params = {"name": name, "save_path": save_path}
                if asset_type == "Blueprint":
                    params["parent_class"] = asset.get("parent_class", "/Script/Engine.Actor")
                    response = unreal.send_command("create_blueprint_class", params)
                elif asset_type == "Level":
                    response = unreal.send_command("create_level", params)
                elif asset_type == "Material":
                    response = unreal.send_command("create_material", params)
                # Add more asset types as needed
                else:
                    response = {"success": False, "message": f"Unsupported asset type: {asset_type}"}
                results.append({"type": asset_type, "name": name, "result": response})
            return {"success": True, "results": results}
        except Exception as e:
            logger.error(f"Error in batch_create_assets: {e}")
            return {"success": False, "message": str(e), "results": results}

    @mcp.tool()
    def batch_delete_assets(ctx: Context, asset_paths: List[str]) -> Dict[str, Any]:
        """
        Batch delete basic assets by asset path.
        Args:
            asset_paths: List of asset paths to delete (e.g., ["/Game/Blueprints/BP_MyActor", ...])
        Returns:
            Dict with success status and a list of results for each asset.
        Example:
            batch_delete_assets(ctx, ["/Game/Blueprints/BP_MyActor"])
        """
        from unreal_mcp_server import get_unreal_connection
        results = []
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine", "results": []}
            for path in asset_paths:
                response = unreal.send_command("delete_asset", {"asset_path": path})
                results.append({"asset_path": path, "result": response})
            return {"success": True, "results": results}
        except Exception as e:
            logger.error(f"Error in batch_delete_assets: {e}")
            return {"success": False, "message": str(e), "results": results}

    @mcp.tool()
    def batch_rename_assets(ctx: Context, renames: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Batch rename basic assets.
        Args:
            renames: List of dicts with keys 'old_path' and 'new_name'. Example:
                [{"old_path": "/Game/Blueprints/BP_MyActor", "new_name": "BP_MyActor2"}, ...]
        Returns:
            Dict with success status and a list of results for each asset.
        Example:
            batch_rename_assets(ctx, [{"old_path": "/Game/Blueprints/BP_MyActor", "new_name": "BP_MyActor2"}])
        """
        from unreal_mcp_server import get_unreal_connection
        results = []
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine", "results": []}
            for rename in renames:
                old_path = rename.get("old_path")
                new_name = rename.get("new_name")
                response = unreal.send_command("rename_asset", {"old_path": old_path, "new_name": new_name})
                results.append({"old_path": old_path, "new_name": new_name, "result": response})
            return {"success": True, "results": results}
        except Exception as e:
            logger.error(f"Error in batch_rename_assets: {e}")
            return {"success": False, "message": str(e), "results": results}

    @mcp.tool()
    def batch_set_asset_properties(ctx: Context, edits: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Batch set properties on basic assets.
        Args:
            edits: List of dicts with keys 'asset_path', 'property_name', and 'property_value'. Example:
                [{"asset_path": "/Game/Blueprints/BP_MyActor", "property_name": "bHidden", "property_value": "True"}, ...]
        Returns:
            Dict with success status and a list of results for each asset.
        Example:
            batch_set_asset_properties(ctx, [{"asset_path": "/Game/Blueprints/BP_MyActor", "property_name": "bHidden", "property_value": "True"}])
        """
        from unreal_mcp_server import get_unreal_connection
        results = []
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine", "results": []}
            for edit in edits:
                asset_path = edit.get("asset_path")
                property_name = edit.get("property_name")
                property_value = edit.get("property_value")
                response = unreal.send_command("set_asset_property", {"asset_path": asset_path, "property_name": property_name, "property_value": property_value})
                results.append({"asset_path": asset_path, "property_name": property_name, "result": response})
            return {"success": True, "results": results}
        except Exception as e:
            logger.error(f"Error in batch_set_asset_properties: {e}")
            return {"success": False, "message": str(e), "results": results} 