"""
Editor Tools for Unreal MCP.

This module provides tools for controlling the Unreal Editor viewport and other editor functionality.
"""

import logging
from typing import Dict, List, Any, Optional
from fastmcp import FastMCP, Context

# Get logger
logger = logging.getLogger("UnrealMCP")

def register_editor_tools(mcp: FastMCP):
    """Register editor tools with the MCP server."""
    
    @mcp.tool()
    def get_actors_in_level(ctx: Context) -> List[Dict[str, Any]]:
        """Get a list of all actors in the current level."""
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.warning("Failed to connect to Unreal Engine")
                return []
                
            response = unreal.send_command("get_actors_in_level", {})
            
            if not response:
                logger.warning("No response from Unreal Engine")
                return []
                
            # Log the complete response for debugging
            logger.info(f"Complete response from Unreal: {response}")
            
            # Check response format
            if "result" in response and "actors" in response["result"]:
                actors = response["result"]["actors"]
                logger.info(f"Found {len(actors)} actors in level")
                return actors
            elif "actors" in response:
                actors = response["actors"]
                logger.info(f"Found {len(actors)} actors in level")
                return actors
                
            logger.warning(f"Unexpected response format: {response}")
            return []
            
        except Exception as e:
            logger.error(f"Error getting actors: {e}")
            return []

    @mcp.tool()
    def find_actors_by_name(ctx: Context, pattern: str) -> List[str]:
        """Find actors by name pattern."""
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.warning("Failed to connect to Unreal Engine")
                return []
                
            response = unreal.send_command("find_actors_by_name", {
                "pattern": pattern
            })
            
            if not response:
                return []
                
            return response.get("actors", [])
            
        except Exception as e:
            logger.error(f"Error finding actors: {e}")
            return []
    
    @mcp.tool()
    def spawn_actor(
        ctx: Context,
        name: str,
        type: str,
        location: List[float] = [0.0, 0.0, 0.0],
        rotation: List[float] = [0.0, 0.0, 0.0],
        scale: List[float] = None
    ) -> Dict[str, Any]:
        """Create a new actor in the current level."""
        from unreal_mcp_server import get_unreal_connection
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            params = {
                "name": name,
                "type": type.upper(),
                "location": location,
                "rotation": rotation
            }
            if scale is not None:
                params["scale"] = scale
            for param_name in ["location", "rotation"]:
                param_value = params[param_name]
                if not isinstance(param_value, list) or len(param_value) != 3:
                    logger.error(f"Invalid {param_name} format: {param_value}. Must be a list of 3 float values.")
                    return {"success": False, "message": f"Invalid {param_name} format. Must be a list of 3 float values."}
                params[param_name] = [float(val) for val in param_value]
            logger.info(f"Creating actor '{name}' of type '{type}' with params: {params}")
            response = unreal.send_command("spawn_actor", params)
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            logger.info(f"Actor creation response: {response}")
            if response.get("status") == "error":
                error_message = response.get("error", "Unknown error")
                logger.error(f"Error creating actor: {error_message}")
                return {"success": False, "message": error_message}
            return response
        except Exception as e:
            error_msg = f"Error creating actor: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    @mcp.tool()
    def delete_actor(ctx: Context, name: str) -> Dict[str, Any]:
        """Delete an actor by name."""
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
                
            response = unreal.send_command("delete_actor", {
                "name": name
            })
            return response or {}
            
        except Exception as e:
            logger.error(f"Error deleting actor: {e}")
            return {}
    
    @mcp.tool()
    def set_actor_transform(
        ctx: Context,
        name: str,
        location: List[float]  = None,
        rotation: List[float]  = None,
        scale: List[float] = None
    ) -> Dict[str, Any]:
        """Set the transform of an actor."""
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
                
            params = {"name": name}
            if location is not None:
                params["location"] = location
            if rotation is not None:
                params["rotation"] = rotation
            if scale is not None:
                params["scale"] = scale
                
            response = unreal.send_command("set_actor_transform", params)
            return response or {}
            
        except Exception as e:
            logger.error(f"Error setting transform: {e}")
            return {}
    
    @mcp.tool()
    def get_actor_properties(ctx: Context, name: str) -> Dict[str, Any]:
        """
        Get all properties of an actor.
        Args:
            name: Name of the actor
        Returns:
            Dict of actor properties
        Example:
            get_actor_properties(ctx, "Cube1")
        """
        from unreal_mcp_server import get_unreal_connection
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            response = unreal.send_command("get_actor_properties", {
                "name": name
            })
            return response or {}
        except Exception as e:
            logger.error(f"Error getting properties: {e}")
            return {}

    @mcp.tool()
    def set_actor_property(
        ctx: Context,
        name: str,
        property_name: str,
        property_value: str,
    ) -> Dict[str, Any]:
        """
        Set a property on an actor.
        Args:
            name: Name of the actor
            property_name: Name of the property to set
            property_value: Value to set the property to (as a string)
        Returns:
            Dict containing response from Unreal with operation status
        Example:
            set_actor_property(ctx, "Cube1", "bHidden", "True")
        """
        from unreal_mcp_server import get_unreal_connection
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            response = unreal.send_command("set_actor_property", {
                "name": name,
                "property_name": property_name,
                "property_value": property_value
            })
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            logger.info(f"Set actor property response: {response}")
            return response
        except Exception as e:
            error_msg = f"Error setting actor property: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}

    # @mcp.tool() commented out because it's buggy
    def focus_viewport(
        ctx: Context,
        target: str = None,
        location: List[float] = None,
        distance: float = 1000.0,
        orientation: List[float] = None
    ) -> Dict[str, Any]:
        """
        Focus the viewport on a specific actor or location.
        
        Args:
            target: Name of the actor to focus on (if provided, location is ignored)
            location: [X, Y, Z] coordinates to focus on (used if target is None)
            distance: Distance from the target/location
            orientation: Optional [Pitch, Yaw, Roll] for the viewport camera
            
        Returns:
            Response from Unreal Engine
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
                
            params = {}
            if target:
                params["target"] = target
            elif location:
                params["location"] = location
            
            if distance:
                params["distance"] = distance
                
            if orientation:
                params["orientation"] = orientation
                
            response = unreal.send_command("focus_viewport", params)
            return response or {}
            
        except Exception as e:
            logger.error(f"Error focusing viewport: {e}")
            return {"status": "error", "message": str(e)}

    @mcp.tool()
    def spawn_blueprint_actor(
        ctx: Context,
        blueprint_name: str,
        actor_name: str,
        location: List[float] = [0.0, 0.0, 0.0],
        rotation: List[float] = [0.0, 0.0, 0.0],
        scale: List[float] = None
    ) -> Dict[str, Any]:
        """Spawn an actor from a Blueprint."""
        from unreal_mcp_server import get_unreal_connection
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            params = {
                "blueprint_name": blueprint_name,
                "actor_name": actor_name,
                "location": location or [0.0, 0.0, 0.0],
                "rotation": rotation or [0.0, 0.0, 0.0]
            }
            if scale is not None:
                params["scale"] = scale
            for param_name in ["location", "rotation"]:
                param_value = params[param_name]
                if not isinstance(param_value, list) or len(param_value) != 3:
                    logger.error(f"Invalid {param_name} format: {param_value}. Must be a list of 3 float values.")
                    return {"success": False, "message": f"Invalid {param_name} format. Must be a list of 3 float values."}
                params[param_name] = [float(val) for val in param_value]
            logger.info(f"Spawning blueprint actor with params: {params}")
            response = unreal.send_command("spawn_blueprint_actor", params)
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            logger.info(f"Spawn blueprint actor response: {response}")
            return response
        except Exception as e:
            error_msg = f"Error spawning blueprint actor: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}

    @mcp.tool()
    def save_level(ctx: Context, level_name: str = None) -> Dict[str, Any]:
        """Save the current or specified level."""
        from unreal_mcp_server import get_unreal_connection
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            params = {"level_name": level_name} if level_name else {}
            response = unreal.send_command("save_level", params)
            return response or {"success": False, "message": "No response from Unreal Engine"}
        except Exception as e:
            logger.error(f"Error saving level: {e}")
            return {"success": False, "message": str(e)}

    @mcp.tool()
    def load_level(ctx: Context, level_name: str) -> Dict[str, Any]:
        """Load a level by name."""
        from unreal_mcp_server import get_unreal_connection
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            response = unreal.send_command("load_level", {"level_name": level_name})
            return response or {"success": False, "message": "No response from Unreal Engine"}
        except Exception as e:
            logger.error(f"Error loading level: {e}")
            return {"success": False, "message": str(e)}

    @mcp.tool()
    def create_level(ctx: Context, level_name: str) -> Dict[str, Any]:
        """Create a new level by name."""
        from unreal_mcp_server import get_unreal_connection
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            response = unreal.send_command("create_level", {"level_name": level_name})
            return response or {"success": False, "message": "No response from Unreal Engine"}
        except Exception as e:
            logger.error(f"Error creating level: {e}")
            return {"success": False, "message": str(e)}

    @mcp.tool()
    def duplicate_level(ctx: Context, source_level: str, new_level: str) -> Dict[str, Any]:
        """Duplicate an existing level."""
        from unreal_mcp_server import get_unreal_connection
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            response = unreal.send_command("duplicate_level", {"source_level": source_level, "new_level": new_level})
            return response or {"success": False, "message": "No response from Unreal Engine"}
        except Exception as e:
            logger.error(f"Error duplicating level: {e}")
            return {"success": False, "message": str(e)}

    @mcp.tool()
    def delete_level(ctx: Context, level_name: str) -> Dict[str, Any]:
        """Delete a level by name."""
        from unreal_mcp_server import get_unreal_connection
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            response = unreal.send_command("delete_level", {"level_name": level_name})
            return response or {"success": False, "message": "No response from Unreal Engine"}
        except Exception as e:
            logger.error(f"Error deleting level: {e}")
            return {"success": False, "message": str(e)}

    @mcp.tool()
    def undo(ctx: Context) -> Dict[str, Any]:
        """Perform an undo action in the editor."""
        from unreal_mcp_server import get_unreal_connection
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            response = unreal.send_command("undo", {})
            return response or {"success": False, "message": "No response from Unreal Engine"}
        except Exception as e:
            logger.error(f"Error performing undo: {e}")
            return {"success": False, "message": str(e)}

    @mcp.tool()
    def redo(ctx: Context) -> Dict[str, Any]:
        """Perform a redo action in the editor."""
        from unreal_mcp_server import get_unreal_connection
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            response = unreal.send_command("redo", {})
            return response or {"success": False, "message": "No response from Unreal Engine"}
        except Exception as e:
            logger.error(f"Error performing redo: {e}")
            return {"success": False, "message": str(e)}

    @mcp.tool()
    def run_editor_command(ctx: Context, command: str, args: Dict[str, str] = None) -> Dict[str, Any]:
        """
        Run a generic editor command (with security checks).
        Args:
            command: Name of the editor command (must be whitelisted)
            args: Dictionary of arguments for the command (optional)
        Returns:
            Dict with success status and command response
        Example:
            run_editor_command(ctx, "rebuild_navigation", {})
        """
        from unreal_mcp_server import get_unreal_connection
        try:
            allowed_commands = {"rebuild_navigation", "build_lighting", "play_in_editor"}
            if command not in allowed_commands:
                logger.error(f"Command '{command}' is not allowed.")
                return {"success": False, "message": f"Command '{command}' is not allowed."}
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            response = unreal.send_command(command, args or {})
            return response or {"success": False, "message": "No response from Unreal Engine"}
        except Exception as e:
            logger.error(f"Error running editor command: {e}")
            return {"success": False, "message": str(e)}

    @mcp.tool()
    def get_world_settings(ctx: Context) -> Dict[str, Any]:
        """
        Get world settings.
        Returns:
            Dict of world settings
        Example:
            get_world_settings(ctx)
        """
        from unreal_mcp_server import get_unreal_connection
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            response = unreal.send_command("get_world_settings", {})
            return response or {"success": False, "message": "No response from Unreal Engine"}
        except Exception as e:
            logger.error(f"Error getting world settings: {e}")
            return {"success": False, "message": str(e)}

    @mcp.tool()
    def set_world_settings(ctx: Context, settings: Dict[str, str]) -> Dict[str, Any]:
        """
        Set world settings.
        Args:
            settings: Dictionary of world settings to set (key-value pairs as strings)
        Returns:
            Dict with success status and response
        Example:
            set_world_settings(ctx, {"GravityZ": "-980.0"})
        """
        from unreal_mcp_server import get_unreal_connection
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            response = unreal.send_command("set_world_settings", {"settings": settings})
            return response or {"success": False, "message": "No response from Unreal Engine"}
        except Exception as e:
            logger.error(f"Error setting world settings: {e}")
            return {"success": False, "message": str(e)}

    @mcp.tool()
    def get_editor_preferences(ctx: Context) -> Dict[str, Any]:
        """
        Get editor preferences.
        Returns:
            Dict of editor preferences
        Example:
            get_editor_preferences(ctx)
        """
        from unreal_mcp_server import get_unreal_connection
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            response = unreal.send_command("get_editor_preferences", {})
            return response or {"success": False, "message": "No response from Unreal Engine"}
        except Exception as e:
            logger.error(f"Error getting editor preferences: {e}")
            return {"success": False, "message": str(e)}

    @mcp.tool()
    def set_editor_preferences(ctx: Context, preferences: Dict[str, str]) -> Dict[str, Any]:
        """
        Set editor preferences.
        Args:
            preferences: Dictionary of editor preferences to set (key-value pairs as strings)
        Returns:
            Dict with success status and response
        Example:
            set_editor_preferences(ctx, {"bShowFPS": "True"})
        """
        from unreal_mcp_server import get_unreal_connection
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            response = unreal.send_command("set_editor_preferences", {"preferences": preferences})
            return response or {"success": False, "message": "No response from Unreal Engine"}
        except Exception as e:
            logger.error(f"Error setting editor preferences: {e}")
            return {"success": False, "message": str(e)}

    @mcp.tool()
    def select_actors(ctx: Context, names: List[str]) -> Dict[str, Any]:
        """
        Select actors in the current level by name.
        Args:
            names: List of actor names to select
        Returns:
            Dict with success status and list of selected actors
        Example:
            select_actors(ctx, ["Cube1", "Sphere2"])
        """
        from unreal_mcp_server import get_unreal_connection
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            response = unreal.send_command("select_actors", {"names": names})
            if not response or response.get("status") != "success":
                logger.error(f"Failed to select actors: {response}")
                return {"success": False, "message": f"Failed to select actors: {response.get('error', 'Unknown error')}", "selected": []}
            selected = response.get("result", {}).get("selected", [])
            return {"success": True, "selected": selected}
        except Exception as e:
            logger.error(f"Error selecting actors: {e}")
            return {"success": False, "message": str(e), "selected": []}

    @mcp.tool()
    def deselect_actors(ctx: Context, names: List[str]) -> Dict[str, Any]:
        """
        Deselect actors in the current level by name.
        Args:
            names: List of actor names to deselect
        Returns:
            Dict with success status and list of remaining selected actors
        Example:
            deselect_actors(ctx, ["Cube1"])
        """
        from unreal_mcp_server import get_unreal_connection
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            response = unreal.send_command("deselect_actors", {"names": names})
            if not response or response.get("status") != "success":
                logger.error(f"Failed to deselect actors: {response}")
                return {"success": False, "message": f"Failed to deselect actors: {response.get('error', 'Unknown error')}", "selected": []}
            selected = response.get("result", {}).get("selected", [])
            return {"success": True, "selected": selected}
        except Exception as e:
            logger.error(f"Error deselecting actors: {e}")
            return {"success": False, "message": str(e), "selected": []}

    @mcp.tool()
    def get_selected_actors(ctx: Context) -> List[str]:
        """
        Get the list of currently selected actors in the editor.
        Returns:
            List of selected actor names
        Example:
            get_selected_actors(ctx)
        """
        from unreal_mcp_server import get_unreal_connection
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return []
            response = unreal.send_command("get_selected_actors", {})
            if not response or response.get("status") != "success":
                logger.error(f"Failed to get selected actors: {response}")
                return []
            return response.get("result", {}).get("selected", [])
        except Exception as e:
            logger.error(f"Error getting selected actors: {e}")
            return []

    logger.info("Editor tools registered successfully")
