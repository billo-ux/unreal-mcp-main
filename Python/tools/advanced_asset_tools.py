"""
Advanced Asset Tools for Unreal MCP.

This module provides tools for creating and managing advanced Unreal Engine assets: Animations, Blend Spaces, Physics Assets, AI, MetaHumans, Data Assets, etc.
"""

import logging
from typing import Dict, List, Any, Optional
from mcp.server.fastmcp import FastMCP, Context
from unreal_mcp_server import get_unreal_connection

logger = logging.getLogger("UnrealMCP")

def register_advanced_asset_tools(mcp: FastMCP):
    """Register advanced asset tools with the MCP server."""
    # ... (tools will be added here in subsequent steps)

    @mcp.tool()
    def create_animation_blueprint(ctx: Context, asset_name: str, skeleton_path: str, parent_class: str = "/Script/Engine.AnimInstance", save_path: str = "/Game/Animations") -> Dict[str, Any]:
        """
        Create an Animation Blueprint asset.
        Args:
            asset_name: Name of the asset to create
            skeleton_path: Path to the skeleton asset
            parent_class: Parent class for the Animation Blueprint
            save_path: Path where the asset will be saved
        Returns:
            Dict containing success status and asset path
        """
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            params = {"asset_name": asset_name, "skeleton_path": skeleton_path, "parent_class": parent_class, "save_path": save_path}
            response = unreal.send_command("create_animation_blueprint", params)
            if not response or response.get("status") != "success":
                logger.error(f"Failed to create Animation Blueprint: {response}")
                return {"success": False, "message": f"Failed to create Animation Blueprint: {response.get('error', 'Unknown error')}"}
            asset_path = response.get("result", {}).get("asset_path", "")
            return {"success": True, "message": f"Successfully created Animation Blueprint: {asset_path}", "asset_path": asset_path}
        except Exception as e:
            logger.error(f"Error creating Animation Blueprint: {e}")
            return {"success": False, "message": str(e)}

    @mcp.tool()
    def create_animation_composite(ctx: Context, asset_name: str, animation_sequences: List[str], save_path: str = "/Game/Animations") -> Dict[str, Any]:
        """
        Create an Animation Composite asset.
        Args:
            asset_name: Name of the asset to create
            animation_sequences: List of animation sequence paths to include
            save_path: Path where the asset will be saved
        Returns:
            Dict containing success status and asset path
        """
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            params = {"asset_name": asset_name, "animation_sequences": animation_sequences, "save_path": save_path}
            response = unreal.send_command("create_animation_composite", params)
            if not response or response.get("status") != "success":
                logger.error(f"Failed to create Animation Composite: {response}")
                return {"success": False, "message": f"Failed to create Animation Composite: {response.get('error', 'Unknown error')}"}
            asset_path = response.get("result", {}).get("asset_path", "")
            return {"success": True, "message": f"Successfully created Animation Composite: {asset_path}", "asset_path": asset_path}
        except Exception as e:
            logger.error(f"Error creating Animation Composite: {e}")
            return {"success": False, "message": str(e)}

    @mcp.tool()
    def create_animation_montage(ctx: Context, asset_name: str, skeleton_path: str, animation_sequence: str = None, save_path: str = "/Game/Animations") -> Dict[str, Any]:
        """
        Create an Animation Montage asset.
        Args:
            asset_name: Name of the asset to create
            skeleton_path: Path to the skeleton asset
            animation_sequence: Optional path to an animation sequence to include
            save_path: Path where the asset will be saved
        Returns:
            Dict containing success status and asset path
        """
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            params = {"asset_name": asset_name, "skeleton_path": skeleton_path, "save_path": save_path}
            if animation_sequence:
                params["animation_sequence"] = animation_sequence
            response = unreal.send_command("create_animation_montage", params)
            if not response or response.get("status") != "success":
                logger.error(f"Failed to create Animation Montage: {response}")
                return {"success": False, "message": f"Failed to create Animation Montage: {response.get('error', 'Unknown error')}"}
            asset_path = response.get("result", {}).get("asset_path", "")
            return {"success": True, "message": f"Successfully created Animation Montage: {asset_path}", "asset_path": asset_path}
        except Exception as e:
            logger.error(f"Error creating Animation Montage: {e}")
            return {"success": False, "message": str(e)}

    @mcp.tool()
    def create_aim_offset(ctx: Context, asset_name: str, skeleton_path: str, save_path: str = "/Game/Animations") -> Dict[str, Any]:
        """
        Create an Aim Offset asset.
        Args:
            asset_name: Name of the asset to create
            skeleton_path: Path to the skeleton asset
            save_path: Path where the asset will be saved
        Returns:
            Dict containing success status and asset path
        """
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            params = {"asset_name": asset_name, "skeleton_path": skeleton_path, "save_path": save_path}
            response = unreal.send_command("create_aim_offset", params)
            if not response or response.get("status") != "success":
                logger.error(f"Failed to create Aim Offset: {response}")
                return {"success": False, "message": f"Failed to create Aim Offset: {response.get('error', 'Unknown error')}"}
            asset_path = response.get("result", {}).get("asset_path", "")
            return {"success": True, "message": f"Successfully created Aim Offset: {asset_path}", "asset_path": asset_path}
        except Exception as e:
            logger.error(f"Error creating Aim Offset: {e}")
            return {"success": False, "message": str(e)}

    @mcp.tool()
    def create_blend_space(ctx: Context, asset_name: str, skeleton_path: str, axis_1_name: str = "Speed", axis_1_min: float = 0.0, axis_1_max: float = 350.0, axis_2_name: str = "Direction", axis_2_min: float = -180.0, axis_2_max: float = 180.0, save_path: str = "/Game/Animations") -> Dict[str, Any]:
        """
        Create a Blend Space asset.
        Args:
            asset_name: Name of the asset to create
            skeleton_path: Path to the skeleton asset
            axis_1_name: Name of the first axis
            axis_1_min: Minimum value for the first axis
            axis_1_max: Maximum value for the first axis
            axis_2_name: Name of the second axis
            axis_2_min: Minimum value for the second axis
            axis_2_max: Maximum value for the second axis
            save_path: Path where the asset will be saved
        Returns:
            Dict containing success status and asset path
        """
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            params = {"asset_name": asset_name, "skeleton_path": skeleton_path, "axis_1_name": axis_1_name, "axis_1_min": axis_1_min, "axis_1_max": axis_1_max, "axis_2_name": axis_2_name, "axis_2_min": axis_2_min, "axis_2_max": axis_2_max, "save_path": save_path}
            response = unreal.send_command("create_blend_space", params)
            if not response or response.get("status") != "success":
                logger.error(f"Failed to create Blend Space: {response}")
                return {"success": False, "message": f"Failed to create Blend Space: {response.get('error', 'Unknown error')}"}
            asset_path = response.get("result", {}).get("asset_path", "")
            return {"success": True, "message": f"Successfully created Blend Space: {asset_path}", "asset_path": asset_path}
        except Exception as e:
            logger.error(f"Error creating Blend Space: {e}")
            return {"success": False, "message": str(e)}

    @mcp.tool()
    def create_pose_asset(ctx: Context, asset_name: str, skeleton_path: str, save_path: str = "/Game/Animations") -> Dict[str, Any]:
        """
        Create a Pose Asset.
        Args:
            asset_name: Name of the asset to create
            skeleton_path: Path to the skeleton asset
            save_path: Path where the asset will be saved
        Returns:
            Dict containing success status and asset path
        """
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            params = {"asset_name": asset_name, "skeleton_path": skeleton_path, "save_path": save_path}
            response = unreal.send_command("create_pose_asset", params)
            if not response or response.get("status") != "success":
                logger.error(f"Failed to create Pose Asset: {response}")
                return {"success": False, "message": f"Failed to create Pose Asset: {response.get('error', 'Unknown error')}"}
            asset_path = response.get("result", {}).get("asset_path", "")
            return {"success": True, "message": f"Successfully created Pose Asset: {asset_path}", "asset_path": asset_path}
        except Exception as e:
            logger.error(f"Error creating Pose Asset: {e}")
            return {"success": False, "message": str(e)}

    @mcp.tool()
    def create_physics_asset(ctx: Context, asset_name: str, skeleton_path: str, save_path: str = "/Game/Physics") -> Dict[str, Any]:
        """
        Create a Physics Asset.
        Args:
            asset_name: Name of the asset to create
            skeleton_path: Path to the skeleton asset
            save_path: Path where the asset will be saved
        Returns:
            Dict containing success status and asset path
        """
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            params = {"asset_name": asset_name, "skeleton_path": skeleton_path, "save_path": save_path}
            response = unreal.send_command("create_physics_asset", params)
            if not response or response.get("status") != "success":
                logger.error(f"Failed to create Physics Asset: {response}")
                return {"success": False, "message": f"Failed to create Physics Asset: {response.get('error', 'Unknown error')}"}
            asset_path = response.get("result", {}).get("asset_path", "")
            return {"success": True, "message": f"Successfully created Physics Asset: {asset_path}", "asset_path": asset_path}
        except Exception as e:
            logger.error(f"Error creating Physics Asset: {e}")
            return {"success": False, "message": str(e)}

    @mcp.tool()
    def create_behavior_tree(ctx: Context, asset_name: str, save_path: str = "/Game/AI") -> Dict[str, Any]:
        """
        Create a Behavior Tree asset.
        Args:
            asset_name: Name of the asset to create
            save_path: Path where the asset will be saved
        Returns:
            Dict containing success status and asset path
        """
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            params = {"asset_name": asset_name, "save_path": save_path}
            response = unreal.send_command("create_behavior_tree", params)
            if not response or response.get("status") != "success":
                logger.error(f"Failed to create Behavior Tree: {response}")
                return {"success": False, "message": f"Failed to create Behavior Tree: {response.get('error', 'Unknown error')}"}
            asset_path = response.get("result", {}).get("asset_path", "")
            return {"success": True, "message": f"Successfully created Behavior Tree: {asset_path}", "asset_path": asset_path}
        except Exception as e:
            logger.error(f"Error creating Behavior Tree: {e}")
            return {"success": False, "message": str(e)}

    @mcp.tool()
    def create_blackboard(ctx: Context, asset_name: str, save_path: str = "/Game/AI") -> Dict[str, Any]:
        """
        Create a Blackboard asset.
        Args:
            asset_name: Name of the asset to create
            save_path: Path where the asset will be saved
        Returns:
            Dict containing success status and asset path
        """
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            params = {"asset_name": asset_name, "save_path": save_path}
            response = unreal.send_command("create_blackboard", params)
            if not response or response.get("status") != "success":
                logger.error(f"Failed to create Blackboard: {response}")
                return {"success": False, "message": f"Failed to create Blackboard: {response.get('error', 'Unknown error')}"}
            asset_path = response.get("result", {}).get("asset_path", "")
            return {"success": True, "message": f"Successfully created Blackboard: {asset_path}", "asset_path": asset_path}
        except Exception as e:
            logger.error(f"Error creating Blackboard: {e}")
            return {"success": False, "message": str(e)}

    @mcp.tool()
    def create_level_sequence(ctx: Context, asset_name: str, save_path: str = "/Game/Cinematics") -> Dict[str, Any]:
        """
        Create a Level Sequence asset.
        Args:
            asset_name: Name of the asset to create
            save_path: Path where the asset will be saved
        Returns:
            Dict containing success status and asset path
        """
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            params = {"asset_name": asset_name, "save_path": save_path}
            response = unreal.send_command("create_level_sequence", params)
            if not response or response.get("status") != "success":
                logger.error(f"Failed to create Level Sequence: {response}")
                return {"success": False, "message": f"Failed to create Level Sequence: {response.get('error', 'Unknown error')}"}
            asset_path = response.get("result", {}).get("asset_path", "")
            return {"success": True, "message": f"Successfully created Level Sequence: {asset_path}", "asset_path": asset_path}
        except Exception as e:
            logger.error(f"Error creating Level Sequence: {e}")
            return {"success": False, "message": str(e)}

    @mcp.tool()
    def create_data_asset(ctx: Context, asset_name: str, parent_class: str, save_path: str = "/Game/Data") -> Dict[str, Any]:
        """
        Create a Data Asset.
        Args:
            asset_name: Name of the asset to create
            parent_class: Parent class for the Data Asset
            save_path: Path where the asset will be saved
        Returns:
            Dict containing success status and asset path
        """
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            params = {"asset_name": asset_name, "parent_class": parent_class, "save_path": save_path}
            response = unreal.send_command("create_data_asset", params)
            if not response or response.get("status") != "success":
                logger.error(f"Failed to create Data Asset: {response}")
                return {"success": False, "message": f"Failed to create Data Asset: {response.get('error', 'Unknown error')}"}
            asset_path = response.get("result", {}).get("asset_path", "")
            return {"success": True, "message": f"Successfully created Data Asset: {asset_path}", "asset_path": asset_path}
        except Exception as e:
            logger.error(f"Error creating Data Asset: {e}")
            return {"success": False, "message": str(e)}

    @mcp.tool()
    def create_game_mode(ctx: Context, asset_name: str, save_path: str = "/Game/Gameplay") -> Dict[str, Any]:
        """
        Create a Game Mode Blueprint.
        Args:
            asset_name: Name of the asset to create
            save_path: Path where the asset will be saved
        Returns:
            Dict containing success status and asset path
        """
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            params = {"asset_name": asset_name, "parent_class": "/Script/Engine.GameModeBase", "save_path": save_path}
            response = unreal.send_command("create_blueprint_class", params)
            if not response or response.get("status") != "success":
                logger.error(f"Failed to create Game Mode: {response}")
                return {"success": False, "message": f"Failed to create Game Mode: {response.get('error', 'Unknown error')}"}
            asset_path = response.get("result", {}).get("asset_path", "")
            return {"success": True, "message": f"Successfully created Game Mode: {asset_path}", "asset_path": asset_path}
        except Exception as e:
            logger.error(f"Error creating Game Mode: {e}")
            return {"success": False, "message": str(e)} 