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

    @mcp.tool()
    def create_animation_layer_interface(ctx: Context, name: str, save_path: str = "/Game/Animations") -> Dict[str, Any]:
        """
        Create an Animation Layer Interface asset.
        Args:
            name: Name of the Animation Layer Interface
            save_path: Path to save the asset
        Returns:
            Dict with success status and asset path
        Note:
            This is a high-complexity asset and may require additional setup in Unreal Editor after creation.
        """
        try:
            params = {"asset_name": name, "save_path": save_path}
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            response = unreal.send_command("create_animation_layer_interface", params)
            if not response or response.get("status") != "success":
                logger.error(f"Failed to create Animation Layer Interface: {response}")
                return {"success": False, "message": f"Failed to create Animation Layer Interface: {response.get('error', 'Unknown error')}"}
            asset_path = response.get("result", {}).get("asset_path", "")
            return {"success": True, "message": f"Successfully created Animation Layer Interface: {asset_path}", "asset_path": asset_path}
        except Exception as e:
            logger.error(f"Error creating Animation Layer Interface: {e}")
            return {"success": False, "message": str(e)}

    @mcp.tool()
    def create_animation_sequence(ctx: Context, name: str, skeleton_path: str, save_path: str = "/Game/Animations") -> Dict[str, Any]:
        """
        Create an Animation Sequence asset.
        Args:
            name: Name of the Animation Sequence
            skeleton_path: Path to the skeleton asset
            save_path: Path to save the asset
        Returns:
            Dict with success status and asset path
        """
        try:
            params = {"asset_name": name, "skeleton_path": skeleton_path, "save_path": save_path}
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            response = unreal.send_command("create_animation_sequence", params)
            if not response or response.get("status") != "success":
                logger.error(f"Failed to create Animation Sequence: {response}")
                return {"success": False, "message": f"Failed to create Animation Sequence: {response.get('error', 'Unknown error')}"}
            asset_path = response.get("result", {}).get("asset_path", "")
            return {"success": True, "message": f"Successfully created Animation Sequence: {asset_path}", "asset_path": asset_path}
        except Exception as e:
            logger.error(f"Error creating Animation Sequence: {e}")
            return {"success": False, "message": str(e)}

    @mcp.tool()
    def create_control_rig(ctx: Context, name: str, save_path: str = "/Game/ControlRigs") -> Dict[str, Any]:
        """
        Create a Control Rig asset.
        Args:
            name: Name of the Control Rig
            save_path: Path to save the asset
        Returns:
            Dict with success status and asset path
        Note:
            This is a high-complexity asset and may require additional setup in Unreal Editor after creation.
        """
        try:
            params = {"asset_name": name, "save_path": save_path}
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            response = unreal.send_command("create_control_rig", params)
            if not response or response.get("status") != "success":
                logger.error(f"Failed to create Control Rig: {response}")
                return {"success": False, "message": f"Failed to create Control Rig: {response.get('error', 'Unknown error')}"}
            asset_path = response.get("result", {}).get("asset_path", "")
            return {"success": True, "message": f"Successfully created Control Rig: {asset_path}", "asset_path": asset_path}
        except Exception as e:
            logger.error(f"Error creating Control Rig: {e}")
            return {"success": False, "message": str(e)}

    @mcp.tool()
    def create_metahuman(ctx: Context, name: str, save_path: str = "/Game/MetaHumans") -> Dict[str, Any]:
        """
        Create a MetaHuman asset.
        Args:
            name: Name of the MetaHuman
            save_path: Path to save the asset
        Returns:
            Dict with success status and asset path
        Note:
            This is a high-complexity asset and may require additional setup in Unreal Editor after creation. MetaHuman creation may require Quixel Bridge integration.
        """
        try:
            params = {"asset_name": name, "save_path": save_path}
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            response = unreal.send_command("create_metahuman", params)
            if not response or response.get("status") != "success":
                logger.error(f"Failed to create MetaHuman: {response}")
                return {"success": False, "message": f"Failed to create MetaHuman: {response.get('error', 'Unknown error')}"}
            asset_path = response.get("result", {}).get("asset_path", "")
            return {"success": True, "message": f"Successfully created MetaHuman: {asset_path}", "asset_path": asset_path}
        except Exception as e:
            logger.error(f"Error creating MetaHuman: {e}")
            return {"success": False, "message": str(e)}

    @mcp.tool()
    def create_sound_mix(ctx: Context, name: str, save_path: str = "/Game/Audio") -> Dict[str, Any]:
        """
        Create a Sound Mix asset.
        Args:
            name: Name of the Sound Mix
            save_path: Path to save the asset
        Returns:
            Dict with success status and asset path
        """
        try:
            params = {"asset_name": name, "save_path": save_path}
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            response = unreal.send_command("create_sound_mix", params)
            if not response or response.get("status") != "success":
                logger.error(f"Failed to create Sound Mix: {response}")
                return {"success": False, "message": f"Failed to create Sound Mix: {response.get('error', 'Unknown error')}"}
            asset_path = response.get("result", {}).get("asset_path", "")
            return {"success": True, "message": f"Successfully created Sound Mix: {asset_path}", "asset_path": asset_path}
        except Exception as e:
            logger.error(f"Error creating Sound Mix: {e}")
            return {"success": False, "message": str(e)}

    @mcp.tool()
    def create_sound_class(ctx: Context, name: str, save_path: str = "/Game/Audio") -> Dict[str, Any]:
        """
        Create a Sound Class asset.
        Args:
            name: Name of the Sound Class
            save_path: Path to save the asset
        Returns:
            Dict with success status and asset path
        """
        try:
            params = {"asset_name": name, "save_path": save_path}
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            response = unreal.send_command("create_sound_class", params)
            if not response or response.get("status") != "success":
                logger.error(f"Failed to create Sound Class: {response}")
                return {"success": False, "message": f"Failed to create Sound Class: {response.get('error', 'Unknown error')}"}
            asset_path = response.get("result", {}).get("asset_path", "")
            return {"success": True, "message": f"Successfully created Sound Class: {asset_path}", "asset_path": asset_path}
        except Exception as e:
            logger.error(f"Error creating Sound Class: {e}")
            return {"success": False, "message": str(e)}

    @mcp.tool()
    def create_media_player(ctx: Context, name: str, save_path: str = "/Game/Media") -> Dict[str, Any]:
        """
        Create a Media Player asset.
        Args:
            name: Name of the Media Player
            save_path: Path to save the asset
        Returns:
            Dict with success status and asset path
        """
        try:
            params = {"asset_name": name, "save_path": save_path}
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            response = unreal.send_command("create_media_player", params)
            if not response or response.get("status") != "success":
                logger.error(f"Failed to create Media Player: {response}")
                return {"success": False, "message": f"Failed to create Media Player: {response.get('error', 'Unknown error')}"}
            asset_path = response.get("result", {}).get("asset_path", "")
            return {"success": True, "message": f"Successfully created Media Player: {asset_path}", "asset_path": asset_path}
        except Exception as e:
            logger.error(f"Error creating Media Player: {e}")
            return {"success": False, "message": str(e)}

    @mcp.tool()
    def create_media_texture(ctx: Context, name: str, media_player: str, save_path: str = "/Game/Media") -> Dict[str, Any]:
        """
        Create a Media Texture asset.
        Args:
            name: Name of the Media Texture
            media_player: Path to the Media Player asset
            save_path: Path to save the asset
        Returns:
            Dict with success status and asset path
        """
        try:
            params = {"asset_name": name, "media_player": media_player, "save_path": save_path}
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            response = unreal.send_command("create_media_texture", params)
            if not response or response.get("status") != "success":
                logger.error(f"Failed to create Media Texture: {response}")
                return {"success": False, "message": f"Failed to create Media Texture: {response.get('error', 'Unknown error')}"}
            asset_path = response.get("result", {}).get("asset_path", "")
            return {"success": True, "message": f"Successfully created Media Texture: {asset_path}", "asset_path": asset_path}
        except Exception as e:
            logger.error(f"Error creating Media Texture: {e}")
            return {"success": False, "message": str(e)}

    @mcp.tool()
    def create_widget_animation(ctx: Context, widget_name: str, animation_name: str, save_path: str = "/Game/UI") -> Dict[str, Any]:
        """
        Create a Widget Animation asset.
        Args:
            widget_name: Name of the widget blueprint
            animation_name: Name of the animation
            save_path: Path to save the asset
        Returns:
            Dict with success status and asset path
        Note:
            Unreal may require additional setup for animation tracks after creation.
        """
        try:
            params = {"widget_name": widget_name, "animation_name": animation_name, "save_path": save_path}
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            response = unreal.send_command("create_widget_animation", params)
            if not response or response.get("status") != "success":
                logger.error(f"Failed to create Widget Animation: {response}")
                return {"success": False, "message": f"Failed to create Widget Animation: {response.get('error', 'Unknown error')}"}
            asset_path = response.get("result", {}).get("asset_path", "")
            return {"success": True, "message": f"Successfully created Widget Animation: {asset_path}", "asset_path": asset_path}
        except Exception as e:
            logger.error(f"Error creating Widget Animation: {e}")
            return {"success": False, "message": str(e)}

    @mcp.tool()
    def create_widget_style_asset(ctx: Context, name: str, save_path: str = "/Game/UI") -> Dict[str, Any]:
        """
        Create a Widget Style asset.
        Args:
            name: Name of the Widget Style asset
            save_path: Path to save the asset
        Returns:
            Dict with success status and asset path
        Note:
            Unreal may require additional setup for style properties after creation.
        """
        try:
            params = {"asset_name": name, "save_path": save_path}
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            response = unreal.send_command("create_widget_style_asset", params)
            if not response or response.get("status") != "success":
                logger.error(f"Failed to create Widget Style Asset: {response}")
                return {"success": False, "message": f"Failed to create Widget Style Asset: {response.get('error', 'Unknown error')}"}
            asset_path = response.get("result", {}).get("asset_path", "")
            return {"success": True, "message": f"Successfully created Widget Style Asset: {asset_path}", "asset_path": asset_path}
        except Exception as e:
            logger.error(f"Error creating Widget Style Asset: {e}")
            return {"success": False, "message": str(e)}

    @mcp.tool()
    def batch_create_advanced_assets(ctx: Context, assets: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Batch create advanced assets.
        Args:
            assets: List of dicts with keys 'type', 'name', and 'save_path'. Example:
                [{"type": "AnimationBlueprint", "name": "ABP_MyAnim", "save_path": "/Game/Animations"}, ...]
        Returns:
            Dict with success status and a list of results for each asset.
        Example:
            batch_create_advanced_assets(ctx, [{"type": "AnimationBlueprint", "name": "ABP_MyAnim", "save_path": "/Game/Animations"}])
        """
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
                params = {"asset_name": name, "save_path": save_path}
                if asset_type == "AnimationBlueprint":
                    params["skeleton_path"] = asset.get("skeleton_path", "")
                    response = unreal.send_command("create_animation_blueprint", params)
                elif asset_type == "PhysicsAsset":
                    params["skeleton_path"] = asset.get("skeleton_path", "")
                    response = unreal.send_command("create_physics_asset", params)
                # Add more advanced asset types as needed
                else:
                    response = {"success": False, "message": f"Unsupported asset type: {asset_type}"}
                results.append({"type": asset_type, "name": name, "result": response})
            return {"success": True, "results": results}
        except Exception as e:
            logger.error(f"Error in batch_create_advanced_assets: {e}")
            return {"success": False, "message": str(e), "results": results}

    @mcp.tool()
    def batch_delete_advanced_assets(ctx: Context, asset_paths: List[str]) -> Dict[str, Any]:
        """
        Batch delete advanced assets by asset path.
        Args:
            asset_paths: List of asset paths to delete (e.g., ["/Game/Animations/ABP_MyAnim", ...])
        Returns:
            Dict with success status and a list of results for each asset.
        Example:
            batch_delete_advanced_assets(ctx, ["/Game/Animations/ABP_MyAnim"])
        """
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
            logger.error(f"Error in batch_delete_advanced_assets: {e}")
            return {"success": False, "message": str(e), "results": results}

    @mcp.tool()
    def batch_rename_advanced_assets(ctx: Context, renames: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Batch rename advanced assets.
        Args:
            renames: List of dicts with keys 'old_path' and 'new_name'. Example:
                [{"old_path": "/Game/Animations/ABP_MyAnim", "new_name": "ABP_MyAnim2"}, ...]
        Returns:
            Dict with success status and a list of results for each asset.
        Example:
            batch_rename_advanced_assets(ctx, [{"old_path": "/Game/Animations/ABP_MyAnim", "new_name": "ABP_MyAnim2"}])
        """
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
            logger.error(f"Error in batch_rename_advanced_assets: {e}")
            return {"success": False, "message": str(e), "results": results}

    @mcp.tool()
    def batch_set_advanced_asset_properties(ctx: Context, edits: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Batch set properties on advanced assets.
        Args:
            edits: List of dicts with keys 'asset_path', 'property_name', and 'property_value'. Example:
                [{"asset_path": "/Game/Animations/ABP_MyAnim", "property_name": "bLooping", "property_value": "True"}, ...]
        Returns:
            Dict with success status and a list of results for each asset.
        Example:
            batch_set_advanced_asset_properties(ctx, [{"asset_path": "/Game/Animations/ABP_MyAnim", "property_name": "bLooping", "property_value": "True"}])
        """
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
            logger.error(f"Error in batch_set_advanced_asset_properties: {e}")
            return {"success": False, "message": str(e), "results": results} 