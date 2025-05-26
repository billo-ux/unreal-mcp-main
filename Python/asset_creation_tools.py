"""
Asset Creation Tools for Unreal MCP.

This module provides tools for creating various Unreal Engine asset types programmatically.
"""

import logging
import os
from typing import Dict, List, Any, Optional
from mcp.server.fastmcp import FastMCP, Context

# Get logger
logger = logging.getLogger("UnrealMCP")

def register_asset_creation_tools(mcp: FastMCP):
    """Register asset creation tools with the MCP server."""
    
    # ==============================
    # Animation Asset Creation Tools
    # ==============================
    
    @mcp.tool()
    def create_animation_blueprint(
        ctx: Context,
        asset_name: str,
        skeleton_path: str,
        parent_class: str = "/Script/Engine.AnimInstance",
        save_path: str = "/Game/Animations"
    ) -> Dict[str, Any]:
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
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {
                "asset_name": asset_name,
                "skeleton_path": skeleton_path,
                "parent_class": parent_class,
                "save_path": save_path
            }
            
            response = unreal.send_command("create_animation_blueprint", params)
            
            if not response or response.get("status") != "success":
                logger.error(f"Failed to create Animation Blueprint: {response}")
                return {"success": False, "message": f"Failed to create Animation Blueprint: {response.get('error', 'Unknown error')}"}
            
            asset_path = response.get("result", {}).get("asset_path", "")
            
            return {
                "success": True,
                "message": f"Successfully created Animation Blueprint: {asset_path}",
                "asset_path": asset_path
            }
            
        except Exception as e:
            error_msg = f"Error creating Animation Blueprint: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    @mcp.tool()
    def create_animation_composite(
        ctx: Context,
        asset_name: str,
        animation_sequences: List[str],
        save_path: str = "/Game/Animations"
    ) -> Dict[str, Any]:
        """
        Create an Animation Composite asset.
        
        Args:
            asset_name: Name of the asset to create
            animation_sequences: List of animation sequence paths to include
            save_path: Path where the asset will be saved
            
        Returns:
            Dict containing success status and asset path
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {
                "asset_name": asset_name,
                "animation_sequences": animation_sequences,
                "save_path": save_path
            }
            
            response = unreal.send_command("create_animation_composite", params)
            
            if not response or response.get("status") != "success":
                logger.error(f"Failed to create Animation Composite: {response}")
                return {"success": False, "message": f"Failed to create Animation Composite: {response.get('error', 'Unknown error')}"}
            
            asset_path = response.get("result", {}).get("asset_path", "")
            
            return {
                "success": True,
                "message": f"Successfully created Animation Composite: {asset_path}",
                "asset_path": asset_path
            }
            
        except Exception as e:
            error_msg = f"Error creating Animation Composite: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    @mcp.tool()
    def create_animation_montage(
        ctx: Context,
        asset_name: str,
        skeleton_path: str,
        animation_sequence: str = None,
        save_path: str = "/Game/Animations"
    ) -> Dict[str, Any]:
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
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {
                "asset_name": asset_name,
                "skeleton_path": skeleton_path,
                "save_path": save_path
            }
            
            if animation_sequence:
                params["animation_sequence"] = animation_sequence
            
            response = unreal.send_command("create_animation_montage", params)
            
            if not response or response.get("status") != "success":
                logger.error(f"Failed to create Animation Montage: {response}")
                return {"success": False, "message": f"Failed to create Animation Montage: {response.get('error', 'Unknown error')}"}
            
            asset_path = response.get("result", {}).get("asset_path", "")
            
            return {
                "success": True,
                "message": f"Successfully created Animation Montage: {asset_path}",
                "asset_path": asset_path
            }
            
        except Exception as e:
            error_msg = f"Error creating Animation Montage: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    @mcp.tool()
    def create_aim_offset(
        ctx: Context,
        asset_name: str,
        skeleton_path: str,
        save_path: str = "/Game/Animations"
    ) -> Dict[str, Any]:
        """
        Create an Aim Offset asset.
        
        Args:
            asset_name: Name of the asset to create
            skeleton_path: Path to the skeleton asset
            save_path: Path where the asset will be saved
            
        Returns:
            Dict containing success status and asset path
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {
                "asset_name": asset_name,
                "skeleton_path": skeleton_path,
                "save_path": save_path
            }
            
            response = unreal.send_command("create_aim_offset", params)
            
            if not response or response.get("status") != "success":
                logger.error(f"Failed to create Aim Offset: {response}")
                return {"success": False, "message": f"Failed to create Aim Offset: {response.get('error', 'Unknown error')}"}
            
            asset_path = response.get("result", {}).get("asset_path", "")
            
            return {
                "success": True,
                "message": f"Successfully created Aim Offset: {asset_path}",
                "asset_path": asset_path
            }
            
        except Exception as e:
            error_msg = f"Error creating Aim Offset: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    @mcp.tool()
    def create_blend_space(
        ctx: Context,
        asset_name: str,
        skeleton_path: str,
        axis_1_name: str = "Speed",
        axis_1_min: float = 0.0,
        axis_1_max: float = 350.0,
        axis_2_name: str = "Direction",
        axis_2_min: float = -180.0,
        axis_2_max: float = 180.0,
        save_path: str = "/Game/Animations"
    ) -> Dict[str, Any]:
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
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {
                "asset_name": asset_name,
                "skeleton_path": skeleton_path,
                "axis_1_name": axis_1_name,
                "axis_1_min": axis_1_min,
                "axis_1_max": axis_1_max,
                "axis_2_name": axis_2_name,
                "axis_2_min": axis_2_min,
                "axis_2_max": axis_2_max,
                "save_path": save_path
            }
            
            response = unreal.send_command("create_blend_space", params)
            
            if not response or response.get("status") != "success":
                logger.error(f"Failed to create Blend Space: {response}")
                return {"success": False, "message": f"Failed to create Blend Space: {response.get('error', 'Unknown error')}"}
            
            asset_path = response.get("result", {}).get("asset_path", "")
            
            return {
                "success": True,
                "message": f"Successfully created Blend Space: {asset_path}",
                "asset_path": asset_path
            }
            
        except Exception as e:
            error_msg = f"Error creating Blend Space: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    @mcp.tool()
    def create_pose_asset(
        ctx: Context,
        asset_name: str,
        skeleton_path: str,
        save_path: str = "/Game/Animations"
    ) -> Dict[str, Any]:
        """
        Create a Pose Asset.
        
        Args:
            asset_name: Name of the asset to create
            skeleton_path: Path to the skeleton asset
            save_path: Path where the asset will be saved
            
        Returns:
            Dict containing success status and asset path
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {
                "asset_name": asset_name,
                "skeleton_path": skeleton_path,
                "save_path": save_path
            }
            
            response = unreal.send_command("create_pose_asset", params)
            
            if not response or response.get("status") != "success":
                logger.error(f"Failed to create Pose Asset: {response}")
                return {"success": False, "message": f"Failed to create Pose Asset: {response.get('error', 'Unknown error')}"}
            
            asset_path = response.get("result", {}).get("asset_path", "")
            
            return {
                "success": True,
                "message": f"Successfully created Pose Asset: {asset_path}",
                "asset_path": asset_path
            }
            
        except Exception as e:
            error_msg = f"Error creating Pose Asset: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    # ==============================
    # Blueprint Asset Creation Tools
    # ==============================
    
    @mcp.tool()
    def create_blueprint_class(
        ctx: Context,
        asset_name: str,
        parent_class: str = "/Script/Engine.Actor",
        save_path: str = "/Game/Blueprints"
    ) -> Dict[str, Any]:
        """
        Create a Blueprint Class asset.
        
        Args:
            asset_name: Name of the asset to create
            parent_class: Parent class for the Blueprint
            save_path: Path where the asset will be saved
            
        Returns:
            Dict containing success status and asset path
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {
                "asset_name": asset_name,
                "parent_class": parent_class,
                "save_path": save_path
            }
            
            response = unreal.send_command("create_blueprint_class", params)
            
            if not response or response.get("status") != "success":
                logger.error(f"Failed to create Blueprint Class: {response}")
                return {"success": False, "message": f"Failed to create Blueprint Class: {response.get('error', 'Unknown error')}"}
            
            asset_path = response.get("result", {}).get("asset_path", "")
            
            return {
                "success": True,
                "message": f"Successfully created Blueprint Class: {asset_path}",
                "asset_path": asset_path
            }
            
        except Exception as e:
            error_msg = f"Error creating Blueprint Class: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    # ==============================
    # Material Asset Creation Tools
    # ==============================
    
    @mcp.tool()
    def create_material(
        ctx: Context,
        asset_name: str,
        save_path: str = "/Game/Materials"
    ) -> Dict[str, Any]:
        """
        Create a Material asset.
        
        Args:
            asset_name: Name of the asset to create
            save_path: Path where the asset will be saved
            
        Returns:
            Dict containing success status and asset path
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {
                "asset_name": asset_name,
                "save_path": save_path
            }
            
            response = unreal.send_command("create_material", params)
            
            if not response or response.get("status") != "success":
                logger.error(f"Failed to create Material: {response}")
                return {"success": False, "message": f"Failed to create Material: {response.get('error', 'Unknown error')}"}
            
            asset_path = response.get("result", {}).get("asset_path", "")
            
            return {
                "success": True,
                "message": f"Successfully created Material: {asset_path}",
                "asset_path": asset_path
            }
            
        except Exception as e:
            error_msg = f"Error creating Material: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    @mcp.tool()
    def create_material_instance(
        ctx: Context,
        asset_name: str,
        parent_material: str,
        save_path: str = "/Game/Materials"
    ) -> Dict[str, Any]:
        """
        Create a Material Instance asset.
        
        Args:
            asset_name: Name of the asset to create
            parent_material: Path to the parent material
            save_path: Path where the asset will be saved
            
        Returns:
            Dict containing success status and asset path
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {
                "asset_name": asset_name,
                "parent_material": parent_material,
                "save_path": save_path
            }
            
            response = unreal.send_command("create_material_instance", params)
            
            if not response or response.get("status") != "success":
                logger.error(f"Failed to create Material Instance: {response}")
                return {"success": False, "message": f"Failed to create Material Instance: {response.get('error', 'Unknown error')}"}
            
            asset_path = response.get("result", {}).get("asset_path", "")
            
            return {
                "success": True,
                "message": f"Successfully created Material Instance: {asset_path}",
                "asset_path": asset_path
            }
            
        except Exception as e:
            error_msg = f"Error creating Material Instance: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    # ==============================
    # Physics Asset Creation Tools
    # ==============================
    
    @mcp.tool()
    def create_physics_asset(
        ctx: Context,
        asset_name: str,
        skeleton_path: str,
        save_path: str = "/Game/Physics"
    ) -> Dict[str, Any]:
        """
        Create a Physics Asset.
        
        Args:
            asset_name: Name of the asset to create
            skeleton_path: Path to the skeleton asset
            save_path: Path where the asset will be saved
            
        Returns:
            Dict containing success status and asset path
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {
                "asset_name": asset_name,
                "skeleton_path": skeleton_path,
                "save_path": save_path
            }
            
            response = unreal.send_command("create_physics_asset", params)
            
            if not response or response.get("status") != "success":
                logger.error(f"Failed to create Physics Asset: {response}")
                return {"success": False, "message": f"Failed to create Physics Asset: {response.get('error', 'Unknown error')}"}
            
            asset_path = response.get("result", {}).get("asset_path", "")
            
            return {
                "success": True,
                "message": f"Successfully created Physics Asset: {asset_path}",
                "asset_path": asset_path
            }
            
        except Exception as e:
            error_msg = f"Error creating Physics Asset: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    # ==============================
    # Artificial Intelligence Tools
    # ==============================
    
    @mcp.tool()
    def create_behavior_tree(
        ctx: Context,
        asset_name: str,
        save_path: str = "/Game/AI"
    ) -> Dict[str, Any]:
        """
        Create a Behavior Tree asset.
        
        Args:
            asset_name: Name of the asset to create
            save_path: Path where the asset will be saved
            
        Returns:
            Dict containing success status and asset path
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {
                "asset_name": asset_name,
                "save_path": save_path
            }
            
            response = unreal.send_command("create_behavior_tree", params)
            
            if not response or response.get("status") != "success":
                logger.error(f"Failed to create Behavior Tree: {response}")
                return {"success": False, "message": f"Failed to create Behavior Tree: {response.get('error', 'Unknown error')}"}
            
            asset_path = response.get("result", {}).get("asset_path", "")
            
            return {
                "success": True,
                "message": f"Successfully created Behavior Tree: {asset_path}",
                "asset_path": asset_path
            }
            
        except Exception as e:
            error_msg = f"Error creating Behavior Tree: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    @mcp.tool()
    def create_blackboard(
        ctx: Context,
        asset_name: str,
        save_path: str = "/Game/AI"
    ) -> Dict[str, Any]:
        """
        Create a Blackboard asset.
        
        Args:
            asset_name: Name of the asset to create
            save_path: Path where the asset will be saved
            
        Returns:
            Dict containing success status and asset path
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {
                "asset_name": asset_name,
                "save_path": save_path
            }
            
            response = unreal.send_command("create_blackboard", params)
            
            if not response or response.get("status") != "success":
                logger.error(f"Failed to create Blackboard: {response}")
                return {"success": False, "message": f"Failed to create Blackboard: {response.get('error', 'Unknown error')}"}
            
            asset_path = response.get("result", {}).get("asset_path", "")
            
            return {
                "success": True,
                "message": f"Successfully created Blackboard: {asset_path}",
                "asset_path": asset_path
            }
            
        except Exception as e:
            error_msg = f"Error creating Blackboard: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    # ==============================
    # Audio Asset Creation Tools
    # ==============================
    
    @mcp.tool()
    def create_sound_cue(
        ctx: Context,
        asset_name: str,
        sound_wave_path: str = None,
        save_path: str = "/Game/Audio"
    ) -> Dict[str, Any]:
        """
        Create a Sound Cue asset.
        
        Args:
            asset_name: Name of the asset to create
            sound_wave_path: Optional path to a sound wave asset
            save_path: Path where the asset will be saved
            
        Returns:
            Dict containing success status and asset path
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {
                "asset_name": asset_name,
                "save_path": save_path
            }
            
            if sound_wave_path:
                params["sound_wave_path"] = sound_wave_path
            
            response = unreal.send_command("create_sound_cue", params)
            
            if not response or response.get("status") != "success":
                logger.error(f"Failed to create Sound Cue: {response}")
                return {"success": False, "message": f"Failed to create Sound Cue: {response.get('error', 'Unknown error')}"}
            
            asset_path = response.get("result", {}).get("asset_path", "")
            
            return {
                "success": True,
                "message": f"Successfully created Sound Cue: {asset_path}",
                "asset_path": asset_path
            }
            
        except Exception as e:
            error_msg = f"Error creating Sound Cue: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    # ==============================
    # Cinematics Asset Creation Tools
    # ==============================
    
    @mcp.tool()
    def create_level_sequence(
        ctx: Context,
        asset_name: str,
        save_path: str = "/Game/Cinematics"
    ) -> Dict[str, Any]:
        """
        Create a Level Sequence asset.
        
        Args:
            asset_name: Name of the asset to create
            save_path: Path where the asset will be saved
            
        Returns:
            Dict containing success status and asset path
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {
                "asset_name": asset_name,
                "save_path": save_path
            }
            
            response = unreal.send_command("create_level_sequence", params)
            
            if not response or response.get("status") != "success":
                logger.error(f"Failed to create Level Sequence: {response}")
                return {"success": False, "message": f"Failed to create Level Sequence: {response.get('error', 'Unknown error')}"}
            
            asset_path = response.get("result", {}).get("asset_path", "")
            
            return {
                "success": True,
                "message": f"Successfully created Level Sequence: {asset_path}",
                "asset_path": asset_path
            }
            
        except Exception as e:
            error_msg = f"Error creating Level Sequence: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    # ==============================
    # User Interface Asset Creation Tools
    # ==============================
    
    @mcp.tool()
    def create_widget_blueprint(
        ctx: Context,
        asset_name: str,
        parent_class: str = "/Script/UMG.UserWidget",
        save_path: str = "/Game/UI"
    ) -> Dict[str, Any]:
        """
        Create a Widget Blueprint asset.
        
        Args:
            asset_name: Name of the asset to create
            parent_class: Parent class for the Widget Blueprint
            save_path: Path where the asset will be saved
            
        Returns:
            Dict containing success status and asset path
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {
                "asset_name": asset_name,
                "parent_class": parent_class,
                "save_path": save_path
            }
            
            response = unreal.send_command("create_widget_blueprint", params)
            
            if not response or response.get("status") != "success":
                logger.error(f"Failed to create Widget Blueprint: {response}")
                return {"success": False, "message": f"Failed to create Widget Blueprint: {response.get('error', 'Unknown error')}"}
            
            asset_path = response.get("result", {}).get("asset_path", "")
            
            return {
                "success": True,
                "message": f"Successfully created Widget Blueprint: {asset_path}",
                "asset_path": asset_path
            }
            
        except Exception as e:
            error_msg = f"Error creating Widget Blueprint: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    # ==============================
    # Niagara Asset Creation Tools
    # ==============================
    
    @mcp.tool()
    def create_niagara_system(
        ctx: Context,
        asset_name: str,
        save_path: str = "/Game/Effects"
    ) -> Dict[str, Any]:
        """
        Create a Niagara System asset.
        
        Args:
            asset_name: Name of the asset to create
            save_path: Path where the asset will be saved
            
        Returns:
            Dict containing success status and asset path
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {
                "asset_name": asset_name,
                "save_path": save_path
            }
            
            response = unreal.send_command("create_niagara_system", params)
            
            if not response or response.get("status") != "success":
                logger.error(f"Failed to create Niagara System: {response}")
                return {"success": False, "message": f"Failed to create Niagara System: {response.get('error', 'Unknown error')}"}
            
            asset_path = response.get("result", {}).get("asset_path", "")
            
            return {
                "success": True,
                "message": f"Successfully created Niagara System: {asset_path}",
                "asset_path": asset_path
            }
            
        except Exception as e:
            error_msg = f"Error creating Niagara System: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    @mcp.tool()
    def create_niagara_emitter(
        ctx: Context,
        asset_name: str,
        save_path: str = "/Game/Effects"
    ) -> Dict[str, Any]:
        """
        Create a Niagara Emitter asset.
        
        Args:
            asset_name: Name of the asset to create
            save_path: Path where the asset will be saved
            
        Returns:
            Dict containing success status and asset path
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {
                "asset_name": asset_name,
                "save_path": save_path
            }
            
            response = unreal.send_command("create_niagara_emitter", params)
            
            if not response or response.get("status") != "success":
                logger.error(f"Failed to create Niagara Emitter: {response}")
                return {"success": False, "message": f"Failed to create Niagara Emitter: {response.get('error', 'Unknown error')}"}
            
            asset_path = response.get("result", {}).get("asset_path", "")
            
            return {
                "success": True,
                "message": f"Successfully created Niagara Emitter: {asset_path}",
                "asset_path": asset_path
            }
            
        except Exception as e:
            error_msg = f"Error creating Niagara Emitter: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    # ==============================
    # Level Asset Creation Tools
    # ==============================
    
    @mcp.tool()
    def create_level(
        ctx: Context,
        asset_name: str,
        template_level: str = None,
        save_path: str = "/Game/Maps"
    ) -> Dict[str, Any]:
        """
        Create a Level asset.
        
        Args:
            asset_name: Name of the asset to create
            template_level: Optional path to a template level
            save_path: Path where the asset will be saved
            
        Returns:
            Dict containing success status and asset path
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {
                "asset_name": asset_name,
                "save_path": save_path
            }
            
            if template_level:
                params["template_level"] = template_level
            
            response = unreal.send_command("create_level", params)
            
            if not response or response.get("status") != "success":
                logger.error(f"Failed to create Level: {response}")
                return {"success": False, "message": f"Failed to create Level: {response.get('error', 'Unknown error')}"}
            
            asset_path = response.get("result", {}).get("asset_path", "")
            
            return {
                "success": True,
                "message": f"Successfully created Level: {asset_path}",
                "asset_path": asset_path
            }
            
        except Exception as e:
            error_msg = f"Error creating Level: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    # ==============================
    # Texture Asset Creation Tools
    # ==============================
    
    @mcp.tool()
    def create_render_target(
        ctx: Context,
        asset_name: str,
        width: int = 1024,
        height: int = 1024,
        save_path: str = "/Game/Textures"
    ) -> Dict[str, Any]:
        """
        Create a Render Target asset.
        
        Args:
            asset_name: Name of the asset to create
            width: Width of the render target
            height: Height of the render target
            save_path: Path where the asset will be saved
            
        Returns:
            Dict containing success status and asset path
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {
                "asset_name": asset_name,
                "width": width,
                "height": height,
                "save_path": save_path
            }
            
            response = unreal.send_command("create_render_target", params)
            
            if not response or response.get("status") != "success":
                logger.error(f"Failed to create Render Target: {response}")
                return {"success": False, "message": f"Failed to create Render Target: {response.get('error', 'Unknown error')}"}
            
            asset_path = response.get("result", {}).get("asset_path", "")
            
            return {
                "success": True,
                "message": f"Successfully created Render Target: {asset_path}",
                "asset_path": asset_path
            }
            
        except Exception as e:
            error_msg = f"Error creating Render Target: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    # ==============================
    # Data Asset Creation Tools
    # ==============================
    
    @mcp.tool()
    def create_data_asset(
        ctx: Context,
        asset_name: str,
        parent_class: str,
        save_path: str = "/Game/Data"
    ) -> Dict[str, Any]:
        """
        Create a Data Asset.
        
        Args:
            asset_name: Name of the asset to create
            parent_class: Parent class for the Data Asset
            save_path: Path where the asset will be saved
            
        Returns:
            Dict containing success status and asset path
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {
                "asset_name": asset_name,
                "parent_class": parent_class,
                "save_path": save_path
            }
            
            response = unreal.send_command("create_data_asset", params)
            
            if not response or response.get("status") != "success":
                logger.error(f"Failed to create Data Asset: {response}")
                return {"success": False, "message": f"Failed to create Data Asset: {response.get('error', 'Unknown error')}"}
            
            asset_path = response.get("result", {}).get("asset_path", "")
            
            return {
                "success": True,
                "message": f"Successfully created Data Asset: {asset_path}",
                "asset_path": asset_path
            }
            
        except Exception as e:
            error_msg = f"Error creating Data Asset: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    # ==============================
    # Gameplay Asset Creation Tools
    # ==============================
    
    @mcp.tool()
    def create_game_mode(
        ctx: Context,
        asset_name: str,
        save_path: str = "/Game/Gameplay"
    ) -> Dict[str, Any]:
        """
        Create a Game Mode Blueprint.
        
        Args:
            asset_name: Name of the asset to create
            save_path: Path where the asset will be saved
            
        Returns:
            Dict containing success status and asset path
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {
                "asset_name": asset_name,
                "parent_class": "/Script/Engine.GameModeBase",
                "save_path": save_path
            }
            
            response = unreal.send_command("create_blueprint_class", params)
            
            if not response or response.get("status") != "success":
                logger.error(f"Failed to create Game Mode: {response}")
                return {"success": False, "message": f"Failed to create Game Mode: {response.get('error', 'Unknown error')}"}
            
            asset_path = response.get("result", {}).get("asset_path", "")
            
            return {
                "success": True,
                "message": f"Successfully created Game Mode: {asset_path}",
                "asset_path": asset_path
            }
            
        except Exception as e:
            error_msg = f"Error creating Game Mode: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    @mcp.tool()
    def create_game_state(
        ctx: Context,
        asset_name: str,
        save_path: str = "/Game/Gameplay"
    ) -> Dict[str, Any]:
        """
        Create a Game State Blueprint.
        
        Args:
            asset_name: Name of the asset to create
            save_path: Path where the asset will be saved
            
        Returns:
            Dict containing success status and asset path
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {
                "asset_name": asset_name,
                "parent_class": "/Script/Engine.GameStateBase",
                "save_path": save_path
            }
            
            response = unreal.send_command("create_blueprint_class", params)
            
            if not response or response.get("status") != "success":
                logger.error(f"Failed to create Game State: {response}")
                return {"success": False, "message": f"Failed to create Game State: {response.get('error', 'Unknown error')}"}
            
            asset_path = response.get("result", {}).get("asset_path", "")
            
            return {
                "success": True,
                "message": f"Successfully created Game State: {asset_path}",
                "asset_path": asset_path
            }
            
        except Exception as e:
            error_msg = f"Error creating Game State: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    @mcp.tool()
    def create_player_controller(
        ctx: Context,
        asset_name: str,
        save_path: str = "/Game/Gameplay"
    ) -> Dict[str, Any]:
        """
        Create a Player Controller Blueprint.
        
        Args:
            asset_name: Name of the asset to create
            save_path: Path where the asset will be saved
            
        Returns:
            Dict containing success status and asset path
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {
                "asset_name": asset_name,
                "parent_class": "/Script/Engine.PlayerController",
                "save_path": save_path
            }
            
            response = unreal.send_command("create_blueprint_class", params)
            
            if not response or response.get("status") != "success":
                logger.error(f"Failed to create Player Controller: {response}")
                return {"success": False, "message": f"Failed to create Player Controller: {response.get('error', 'Unknown error')}"}
            
            asset_path = response.get("result", {}).get("asset_path", "")
            
            return {
                "success": True,
                "message": f"Successfully created Player Controller: {asset_path}",
                "asset_path": asset_path
            }
            
        except Exception as e:
            error_msg = f"Error creating Player Controller: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    logger.info("Asset creation tools registered successfully")
