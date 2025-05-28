"""
Enhanced Node Tools for Unreal MCP.

This module provides advanced tools for Blueprint node management, including precise actor placement
and complete event graph logic creation.
"""

import logging
import os
from typing import Dict, List, Any, Optional, Tuple
from mcp.server.fastmcp import FastMCP, Context

# Get logger
logger = logging.getLogger("UnrealMCP")

def register_enhanced_node_tools(mcp: FastMCP):
    """Register enhanced Blueprint node tools with the MCP server."""
    
    @mcp.tool()
    def create_rotating_actor(
        ctx: Context,
        actor_type: str = "Cube",
        blueprint_name: str = None,
        location: List[float] = None,
        rotation: List[float] = None,
        scale: List[float] = None,
        rotation_speed: float = 20.0,
        rotation_axis: str = "Z",
        spawn_in_level_editor: bool = True
    ) -> Dict[str, Any]:
        """
        Create an actor that rotates continuously.
        
        Args:
            actor_type: Type of actor to create ("Cube", "Sphere", "Cylinder", etc.)
            blueprint_name: Optional name for the Blueprint to create (if None, will generate one)
            location: Optional location [X, Y, Z]
            rotation: Optional rotation [Pitch, Yaw, Roll]
            scale: Optional scale [X, Y, Z] (default: [1,1,1] if not provided)
            rotation_speed: Speed of rotation in degrees per second
            rotation_axis: Axis to rotate around ("X", "Y", or "Z")
            spawn_in_level_editor: If True, spawn the actor in the level editor; if False, do not spawn automatically (e.g., for BeginPlay logic only)
        
        Returns:
            Dict containing success status and actor details
        
        Example:
            create_rotating_actor(ctx, actor_type="Cube", spawn_in_level_editor=True)
        """
        # This edit follows the 'tools' Cursor rule for MCP tools.
        from unreal_mcp_server import get_unreal_connection
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            # Default values
            if location is None:
                location = [0, 0, 0]
            if rotation is None:
                rotation = [0, 0, 0]
            if scale is None:
                scale = [1.0, 1.0, 1.0]
            # Generate Blueprint name if not provided
            if blueprint_name is None:
                blueprint_name = f"BP_Rotating_{actor_type}"
            
            # Create the Blueprint
            blueprint_params = {
                "blueprint_name": blueprint_name,
                "parent_class": "/Script/Engine.Actor",
                "save_path": "/Game/Blueprints"
            }
            
            blueprint_response = unreal.send_command("create_blueprint_class", blueprint_params)
            
            if not blueprint_response or blueprint_response.get("status") != "success":
                logger.error(f"Failed to create Blueprint: {blueprint_response}")
                return {"success": False, "message": f"Failed to create Blueprint: {blueprint_response.get('error', 'Unknown error')}"}
            
            # Add a static mesh component
            component_params = {
                "blueprint_name": blueprint_name,
                "component_type": "StaticMeshComponent",
                "component_name": f"{actor_type}Mesh"
            }
            
            component_response = unreal.send_command("add_component_to_blueprint", component_params)
            
            if not component_response or component_response.get("status") != "success":
                logger.error(f"Failed to add component: {component_response}")
                return {"success": False, "message": f"Failed to add component: {component_response.get('error', 'Unknown error')}"}
            
            # Set the static mesh based on actor type
            mesh_path = ""
            if actor_type.lower() == "cube":
                mesh_path = "/Engine/BasicShapes/Cube.Cube"
            elif actor_type.lower() == "sphere":
                mesh_path = "/Engine/BasicShapes/Sphere.Sphere"
            elif actor_type.lower() == "cylinder":
                mesh_path = "/Engine/BasicShapes/Cylinder.Cylinder"
            elif actor_type.lower() == "cone":
                mesh_path = "/Engine/BasicShapes/Cone.Cone"
            else:
                mesh_path = "/Engine/BasicShapes/Cube.Cube"  # Default to cube
            
            mesh_params = {
                "blueprint_name": blueprint_name,
                "component_name": f"{actor_type}Mesh",
                "static_mesh": mesh_path
            }
            
            mesh_response = unreal.send_command("set_static_mesh_properties", mesh_params)
            
            if not mesh_response or mesh_response.get("status") != "success":
                logger.error(f"Failed to set static mesh: {mesh_response}")
                return {"success": False, "message": f"Failed to set static mesh: {mesh_response.get('error', 'Unknown error')}"}
            
            # Create the rotation logic in the event graph
            
            # 1. Add the Event Tick node
            tick_params = {
                "blueprint_name": blueprint_name,
                "event_type": "EventTick"
            }
            
            tick_response = unreal.send_command("add_blueprint_event_node", tick_params)
            
            if not tick_response or tick_response.get("status") != "success":
                logger.error(f"Failed to add Event Tick node: {tick_response}")
                return {"success": False, "message": f"Failed to add Event Tick node: {tick_response.get('error', 'Unknown error')}"}
            
            tick_node_id = tick_response.get("result", {}).get("node_id")
            
            # 2. Add the Get Delta Seconds node
            delta_params = {
                "blueprint_name": blueprint_name,
                "function": "GetWorldDeltaSeconds",
                "target": "self"
            }
            
            delta_response = unreal.send_command("add_blueprint_function_call_node", delta_params)
            
            if not delta_response or delta_response.get("status") != "success":
                logger.error(f"Failed to add Get Delta Seconds node: {delta_response}")
                return {"success": False, "message": f"Failed to add Get Delta Seconds node: {delta_response.get('error', 'Unknown error')}"}
            
            delta_node_id = delta_response.get("result", {}).get("node_id")
            
            # 3. Add a multiply node for rotation speed
            multiply_params = {
                "blueprint_name": blueprint_name,
                "operation": "float * float",
                "position": [400, 0]
            }
            
            multiply_response = unreal.send_command("add_blueprint_math_node", multiply_params)
            
            if not multiply_response or multiply_response.get("status") != "success":
                logger.error(f"Failed to add multiply node: {multiply_response}")
                return {"success": False, "message": f"Failed to add multiply node: {multiply_response.get('error', 'Unknown error')}"}
            
            multiply_node_id = multiply_response.get("result", {}).get("node_id")
            
            # 4. Set the rotation speed constant
            speed_params = {
                "blueprint_name": blueprint_name,
                "node_id": multiply_node_id,
                "pin_name": "B",
                "value": str(rotation_speed)
            }
            
            speed_response = unreal.send_command("set_blueprint_node_pin_value", speed_params)
            
            if not speed_response or speed_response.get("status") != "success":
                logger.error(f"Failed to set rotation speed: {speed_response}")
                return {"success": False, "message": f"Failed to set rotation speed: {speed_response.get('error', 'Unknown error')}"}
            
            # 5. Create a rotation vector
            make_rot_params = {
                "blueprint_name": blueprint_name,
                "function": "MakeRotator",
                "position": [600, 0]
            }
            
            make_rot_response = unreal.send_command("add_blueprint_function_call_node", make_rot_params)
            
            if not make_rot_response or make_rot_response.get("status") != "success":
                logger.error(f"Failed to add Make Rotator node: {make_rot_response}")
                return {"success": False, "message": f"Failed to add Make Rotator node: {make_rot_response.get('error', 'Unknown error')}"}
            
            make_rot_node_id = make_rot_response.get("result", {}).get("node_id")
            
            # 6. Set the rotation axis
            rot_x = "0"
            rot_y = "0"
            rot_z = "0"
            
            if rotation_axis.upper() == "X":
                rot_x = "1"
            elif rotation_axis.upper() == "Y":
                rot_y = "1"
            else:  # Default to Z
                rot_z = "1"
            
            # Set X rotation
            rot_x_params = {
                "blueprint_name": blueprint_name,
                "node_id": make_rot_node_id,
                "pin_name": "Roll",
                "value": rot_x
            }
            
            rot_x_response = unreal.send_command("set_blueprint_node_pin_value", rot_x_params)
            
            if not rot_x_response or rot_x_response.get("status") != "success":
                logger.error(f"Failed to set X rotation: {rot_x_response}")
                return {"success": False, "message": f"Failed to set X rotation: {rot_x_response.get('error', 'Unknown error')}"}
            
            # Set Y rotation
            rot_y_params = {
                "blueprint_name": blueprint_name,
                "node_id": make_rot_node_id,
                "pin_name": "Pitch",
                "value": rot_y
            }
            
            rot_y_response = unreal.send_command("set_blueprint_node_pin_value", rot_y_params)
            
            if not rot_y_response or rot_y_response.get("status") != "success":
                logger.error(f"Failed to set Y rotation: {rot_y_response}")
                return {"success": False, "message": f"Failed to set Y rotation: {rot_y_response.get('error', 'Unknown error')}"}
            
            # Set Z rotation
            rot_z_params = {
                "blueprint_name": blueprint_name,
                "node_id": make_rot_node_id,
                "pin_name": "Yaw",
                "value": rot_z
            }
            
            rot_z_response = unreal.send_command("set_blueprint_node_pin_value", rot_z_params)
            
            if not rot_z_response or rot_z_response.get("status") != "success":
                logger.error(f"Failed to set Z rotation: {rot_z_response}")
                return {"success": False, "message": f"Failed to set Z rotation: {rot_z_response.get('error', 'Unknown error')}"}
            
            # 7. Add the Add Actor Local Rotation node
            add_rot_params = {
                "blueprint_name": blueprint_name,
                "function": "AddActorLocalRotation",
                "target": "self",
                "position": [800, 0]
            }
            
            add_rot_response = unreal.send_command("add_blueprint_function_call_node", add_rot_params)
            
            if not add_rot_response or add_rot_response.get("status") != "success":
                logger.error(f"Failed to add Add Actor Local Rotation node: {add_rot_response}")
                return {"success": False, "message": f"Failed to add Add Actor Local Rotation node: {add_rot_response.get('error', 'Unknown error')}"}
            
            add_rot_node_id = add_rot_response.get("result", {}).get("node_id")
            
            # 8. Connect the nodes
            
            # Connect Event Tick to Get Delta Seconds
            connect_tick_delta_params = {
                "blueprint_name": blueprint_name,
                "source_node_id": tick_node_id,
                "source_pin": "ExecutionOutput",
                "target_node_id": delta_node_id,
                "target_pin": "ExecutionInput"
            }
            
            connect_tick_delta_response = unreal.send_command("connect_blueprint_nodes", connect_tick_delta_params)
            
            if not connect_tick_delta_response or connect_tick_delta_response.get("status") != "success":
                logger.error(f"Failed to connect Event Tick to Get Delta Seconds: {connect_tick_delta_response}")
                return {"success": False, "message": f"Failed to connect Event Tick to Get Delta Seconds: {connect_tick_delta_response.get('error', 'Unknown error')}"}
            
            # Connect Get Delta Seconds to Multiply
            connect_delta_multiply_params = {
                "blueprint_name": blueprint_name,
                "source_node_id": delta_node_id,
                "source_pin": "ReturnValue",
                "target_node_id": multiply_node_id,
                "target_pin": "A"
            }
            
            connect_delta_multiply_response = unreal.send_command("connect_blueprint_nodes", connect_delta_multiply_params)
            
            if not connect_delta_multiply_response or connect_delta_multiply_response.get("status") != "success":
                logger.error(f"Failed to connect Get Delta Seconds to Multiply: {connect_delta_multiply_response}")
                return {"success": False, "message": f"Failed to connect Get Delta Seconds to Multiply: {connect_delta_multiply_response.get('error', 'Unknown error')}"}
            
            # Connect Multiply to Make Rotator
            # Determine the correct pin name for the rotation axis
            if rotation_axis.upper() == "X":
                rot_pin = "Roll"
            elif rotation_axis.upper() == "Y":
                rot_pin = "Pitch"
            else:
                rot_pin = "Yaw"
            connect_multiply_rot_params = {
                "blueprint_name": blueprint_name,
                "source_node_id": multiply_node_id,
                "source_pin": "ReturnValue",
                "target_node_id": make_rot_node_id,
                "target_pin": rot_pin
            }
            
            connect_multiply_rot_response = unreal.send_command("connect_blueprint_nodes", connect_multiply_rot_params)
            
            if not connect_multiply_rot_response or connect_multiply_rot_response.get("status") != "success":
                logger.error(f"Failed to connect Multiply to Make Rotator: {connect_multiply_rot_response}")
                return {"success": False, "message": f"Failed to connect Multiply to Make Rotator: {connect_multiply_rot_response.get('error', 'Unknown error')}"}
            
            # Connect Make Rotator to Add Actor Local Rotation
            connect_rot_add_rot_params = {
                "blueprint_name": blueprint_name,
                "source_node_id": make_rot_node_id,
                "source_pin": "ReturnValue",
                "target_node_id": add_rot_node_id,
                "target_pin": "DeltaRotation"
            }
            
            connect_rot_add_rot_response = unreal.send_command("connect_blueprint_nodes", connect_rot_add_rot_params)
            
            if not connect_rot_add_rot_response or connect_rot_add_rot_response.get("status") != "success":
                logger.error(f"Failed to connect Make Rotator to Add Actor Local Rotation: {connect_rot_add_rot_response}")
                return {"success": False, "message": f"Failed to connect Make Rotator to Add Actor Local Rotation: {connect_rot_add_rot_response.get('error', 'Unknown error')}"}
            
            # Connect Get Delta Seconds to Add Actor Local Rotation (execution flow)
            connect_delta_add_rot_params = {
                "blueprint_name": blueprint_name,
                "source_node_id": delta_node_id,
                "source_pin": "ExecutionOutput",
                "target_node_id": add_rot_node_id,
                "target_pin": "ExecutionInput"
            }
            
            connect_delta_add_rot_response = unreal.send_command("connect_blueprint_nodes", connect_delta_add_rot_params)
            
            if not connect_delta_add_rot_response or connect_delta_add_rot_response.get("status") != "success":
                logger.error(f"Failed to connect Get Delta Seconds to Add Actor Local Rotation: {connect_delta_add_rot_response}")
                return {"success": False, "message": f"Failed to connect Get Delta Seconds to Add Actor Local Rotation: {connect_delta_add_rot_response.get('error', 'Unknown error')}"}
            
            # Compile the Blueprint
            compile_params = {
                "blueprint_name": blueprint_name
            }
            
            compile_response = unreal.send_command("compile_blueprint", compile_params)
            
            if not compile_response or compile_response.get("status") != "success":
                logger.error(f"Failed to compile Blueprint: {compile_response}")
                return {"success": False, "message": f"Failed to compile Blueprint: {compile_response.get('error', 'Unknown error')}"}
            
            # Only spawn in the level editor if requested
            if spawn_in_level_editor:
                spawn_params = {
                    "blueprint_name": blueprint_name,
                    "actor_name": f"Rotating{actor_type}",
                    "location": location,
                    "rotation": rotation,
                    "scale": scale
                }
                spawn_response = unreal.send_command("spawn_blueprint_actor", spawn_params)
                if not spawn_response or spawn_response.get("status") != "success":
                    logger.error(f"Failed to spawn actor: {spawn_response}")
                    return {"success": False, "message": f"Failed to spawn actor: {spawn_response.get('error', 'Unknown error')}"}
                actor_name = spawn_response.get("result", {}).get("actor_name", "")
            else:
                actor_name = None
            return {
                "success": True,
                "message": f"Successfully created rotating {actor_type} Blueprint.",
                "blueprint_name": blueprint_name,
                "actor_name": actor_name,
                "location": location,
                "rotation": rotation,
                "scale": scale,
                "rotation_speed": rotation_speed,
                "rotation_axis": rotation_axis,
                "spawn_in_level_editor": spawn_in_level_editor
            }
            
        except Exception as e:
            error_msg = f"Error creating rotating actor: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    @mcp.tool()
    def add_blueprint_complete_rotation_logic(
        ctx: Context,
        blueprint_name: str,
        rotation_speed: float = 20.0,
        rotation_axis: str = "Z"
    ) -> Dict[str, Any]:
        """
        Add complete rotation logic to an existing Blueprint.
        
        Args:
            blueprint_name: Name of the target Blueprint
            rotation_speed: Speed of rotation in degrees per second
            rotation_axis: Axis to rotate around ("X", "Y", or "Z")
            
        Returns:
            Dict containing success status and details
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            # 1. Add the Event Tick node
            tick_params = {
                "blueprint_name": blueprint_name,
                "event_type": "EventTick"
            }
            
            tick_response = unreal.send_command("add_blueprint_event_node", tick_params)
            
            if not tick_response or tick_response.get("status") != "success":
                logger.error(f"Failed to add Event Tick node: {tick_response}")
                return {"success": False, "message": f"Failed to add Event Tick node: {tick_response.get('error', 'Unknown error')}"}
            
            tick_node_id = tick_response.get("result", {}).get("node_id")
            
            # 2. Add the Get Delta Seconds node
            delta_params = {
                "blueprint_name": blueprint_name,
                "function": "GetWorldDeltaSeconds",
                "target": "self"
            }
            
            delta_response = unreal.send_command("add_blueprint_function_call_node", delta_params)
            
            if not delta_response or delta_response.get("status") != "success":
                logger.error(f"Failed to add Get Delta Seconds node: {delta_response}")
                return {"success": False, "message": f"Failed to add Get Delta Seconds node: {delta_response.get('error', 'Unknown error')}"}
            
            delta_node_id = delta_response.get("result", {}).get("node_id")
            
            # 3. Add a multiply node for rotation speed
            multiply_params = {
                "blueprint_name": blueprint_name,
                "operation": "float * float",
                "position": [400, 0]
            }
            
            multiply_response = unreal.send_command("add_blueprint_math_node", multiply_params)
            
            if not multiply_response or multiply_response.get("status") != "success":
                logger.error(f"Failed to add multiply node: {multiply_response}")
                return {"success": False, "message": f"Failed to add multiply node: {multiply_response.get('error', 'Unknown error')}"}
            
            multiply_node_id = multiply_response.get("result", {}).get("node_id")
            
            # 4. Set the rotation speed constant
            speed_params = {
                "blueprint_name": blueprint_name,
                "node_id": multiply_node_id,
                "pin_name": "B",
                "value": str(rotation_speed)
            }
            
            speed_response = unreal.send_command("set_blueprint_node_pin_value", speed_params)
            
            if not speed_response or speed_response.get("status") != "success":
                logger.error(f"Failed to set rotation speed: {speed_response}")
                return {"success": False, "message": f"Failed to set rotation speed: {speed_response.get('error', 'Unknown error')}"}
            
            # 5. Create a rotation vector
            make_rot_params = {
                "blueprint_name": blueprint_name,
                "function": "MakeRotator",
                "position": [600, 0]
            }
            
            make_rot_response = unreal.send_command("add_blueprint_function_call_node", make_rot_params)
            
            if not make_rot_response or make_rot_response.get("status") != "success":
                logger.error(f"Failed to add Make Rotator node: {make_rot_response}")
                return {"success": False, "message": f"Failed to add Make Rotator node: {make_rot_response.get('error', 'Unknown error')}"}
            
            make_rot_node_id = make_rot_response.get("result", {}).get("node_id")
            
            # 6. Set the rotation axis
            rot_x = "0"
            rot_y = "0"
            rot_z = "0"
            
            if rotation_axis.upper() == "X":
                rot_x = "1"
            elif rotation_axis.upper() == "Y":
                rot_y = "1"
            else:  # Default to Z
                rot_z = "1"
            
            # Set X rotation
            rot_x_params = {
                "blueprint_name": blueprint_name,
                "node_id": make_rot_node_id,
                "pin_name": "Roll",
                "value": rot_x
            }
            
            rot_x_response = unreal.send_command("set_blueprint_node_pin_value", rot_x_params)
            
            if not rot_x_response or rot_x_response.get("status") != "success":
                logger.error(f"Failed to set X rotation: {rot_x_response}")
                return {"success": False, "message": f"Failed to set X rotation: {rot_x_response.get('error', 'Unknown error')}"}
            
            # Set Y rotation
            rot_y_params = {
                "blueprint_name": blueprint_name,
                "node_id": make_rot_node_id,
                "pin_name": "Pitch",
                "value": rot_y
            }
            
            rot_y_response = unreal.send_command("set_blueprint_node_pin_value", rot_y_params)
            
            if not rot_y_response or rot_y_response.get("status") != "success":
                logger.error(f"Failed to set Y rotation: {rot_y_response}")
                return {"success": False, "message": f"Failed to set Y rotation: {rot_y_response.get('error', 'Unknown error')}"}
            
            # Set Z rotation
            rot_z_params = {
                "blueprint_name": blueprint_name,
                "node_id": make_rot_node_id,
                "pin_name": "Yaw",
                "value": rot_z
            }
            
            rot_z_response = unreal.send_command("set_blueprint_node_pin_value", rot_z_params)
            
            if not rot_z_response or rot_z_response.get("status") != "success":
                logger.error(f"Failed to set Z rotation: {rot_z_response}")
                return {"success": False, "message": f"Failed to set Z rotation: {rot_z_response.get('error', 'Unknown error')}"}
            
            # 7. Add the Add Actor Local Rotation node
            add_rot_params = {
                "blueprint_name": blueprint_name,
                "function": "AddActorLocalRotation",
                "target": "self",
                "position": [800, 0]
            }
            
            add_rot_response = unreal.send_command("add_blueprint_function_call_node", add_rot_params)
            
            if not add_rot_response or add_rot_response.get("status") != "success":
                logger.error(f"Failed to add Add Actor Local Rotation node: {add_rot_response}")
                return {"success": False, "message": f"Failed to add Add Actor Local Rotation node: {add_rot_response.get('error', 'Unknown error')}"}
            
            add_rot_node_id = add_rot_response.get("result", {}).get("node_id")
            
            # 8. Connect the nodes
            
            # Connect Event Tick to Get Delta Seconds
            connect_tick_delta_params = {
                "blueprint_name": blueprint_name,
                "source_node_id": tick_node_id,
                "source_pin": "ExecutionOutput",
                "target_node_id": delta_node_id,
                "target_pin": "ExecutionInput"
            }
            
            connect_tick_delta_response = unreal.send_command("connect_blueprint_nodes", connect_tick_delta_params)
            
            if not connect_tick_delta_response or connect_tick_delta_response.get("status") != "success":
                logger.error(f"Failed to connect Event Tick to Get Delta Seconds: {connect_tick_delta_response}")
                return {"success": False, "message": f"Failed to connect Event Tick to Get Delta Seconds: {connect_tick_delta_response.get('error', 'Unknown error')}"}
            
            # Connect Get Delta Seconds to Multiply
            connect_delta_multiply_params = {
                "blueprint_name": blueprint_name,
                "source_node_id": delta_node_id,
                "source_pin": "ReturnValue",
                "target_node_id": multiply_node_id,
                "target_pin": "A"
            }
            
            connect_delta_multiply_response = unreal.send_command("connect_blueprint_nodes", connect_delta_multiply_params)
            
            if not connect_delta_multiply_response or connect_delta_multiply_response.get("status") != "success":
                logger.error(f"Failed to connect Get Delta Seconds to Multiply: {connect_delta_multiply_response}")
                return {"success": False, "message": f"Failed to connect Get Delta Seconds to Multiply: {connect_delta_multiply_response.get('error', 'Unknown error')}"}
            
            # Connect Multiply to Make Rotator
            rot_pin = "Yaw"  # Default to Z
            if rotation_axis.upper() == "X":
                rot_pin = "Roll"
            elif rotation_axis.upper() == "Y":
                rot_pin = "Pitch"
            
            connect_multiply_rot_params = {
                "blueprint_name": blueprint_name,
                "source_node_id": multiply_node_id,
                "source_pin": "ReturnValue",
                "target_node_id": make_rot_node_id,
                "target_pin": rot_pin
            }
            
            connect_multiply_rot_response = unreal.send_command("connect_blueprint_nodes", connect_multiply_rot_params)
            
            if not connect_multiply_rot_response or connect_multiply_rot_response.get("status") != "success":
                logger.error(f"Failed to connect Multiply to Make Rotator: {connect_multiply_rot_response}")
                return {"success": False, "message": f"Failed to connect Multiply to Make Rotator: {connect_multiply_rot_response.get('error', 'Unknown error')}"}
            
            # Connect Make Rotator to Add Actor Local Rotation
            connect_rot_add_rot_params = {
                "blueprint_name": blueprint_name,
                "source_node_id": make_rot_node_id,
                "source_pin": "ReturnValue",
                "target_node_id": add_rot_node_id,
                "target_pin": "DeltaRotation"
            }
            
            connect_rot_add_rot_response = unreal.send_command("connect_blueprint_nodes", connect_rot_add_rot_params)
            
            if not connect_rot_add_rot_response or connect_rot_add_rot_response.get("status") != "success":
                logger.error(f"Failed to connect Make Rotator to Add Actor Local Rotation: {connect_rot_add_rot_response}")
                return {"success": False, "message": f"Failed to connect Make Rotator to Add Actor Local Rotation: {connect_rot_add_rot_response.get('error', 'Unknown error')}"}
            
            # Connect Get Delta Seconds to Add Actor Local Rotation (execution flow)
            connect_delta_add_rot_params = {
                "blueprint_name": blueprint_name,
                "source_node_id": delta_node_id,
                "source_pin": "ExecutionOutput",
                "target_node_id": add_rot_node_id,
                "target_pin": "ExecutionInput"
            }
            
            connect_delta_add_rot_response = unreal.send_command("connect_blueprint_nodes", connect_delta_add_rot_params)
            
            if not connect_delta_add_rot_response or connect_delta_add_rot_response.get("status") != "success":
                logger.error(f"Failed to connect Get Delta Seconds to Add Actor Local Rotation: {connect_delta_add_rot_response}")
                return {"success": False, "message": f"Failed to connect Get Delta Seconds to Add Actor Local Rotation: {connect_delta_add_rot_response.get('error', 'Unknown error')}"}
            
            # Compile the Blueprint
            compile_params = {
                "blueprint_name": blueprint_name
            }
            
            compile_response = unreal.send_command("compile_blueprint", compile_params)
            
            if not compile_response or compile_response.get("status") != "success":
                logger.error(f"Failed to compile Blueprint: {compile_response}")
                return {"success": False, "message": f"Failed to compile Blueprint: {compile_response.get('error', 'Unknown error')}"}
            
            return {
                "success": True,
                "message": f"Successfully added rotation logic to {blueprint_name}",
                "blueprint_name": blueprint_name,
                "rotation_speed": rotation_speed,
                "rotation_axis": rotation_axis
            }
            
        except Exception as e:
            error_msg = f"Error adding rotation logic: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    @mcp.tool()
    def create_precise_actor_at_location(
        ctx: Context,
        actor_type: str,
        location: List[float] = None,
        rotation: List[float] = None,
        scale: List[float] = None,
        actor_name: str = None,
        blueprint_name: str = None,
        use_blueprint: bool = False
    ) -> Dict[str, Any]:
        """
        Create an actor at a precise location.
        
        Args:
            actor_type: Type of actor to create ("Cube", "Sphere", "Cylinder", etc.)
            location: Optional location [X, Y, Z]
            rotation: Optional rotation [Pitch, Yaw, Roll]
            scale: Optional scale [X, Y, Z]
            actor_name: Optional name for the actor
            blueprint_name: Optional name for the Blueprint to create (if use_blueprint is True)
            use_blueprint: Whether to create a Blueprint for the actor
            
        Returns:
            Dict containing success status and actor details
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            # Default values
            if location is None:
                location = [0, 0, 0]
            if rotation is None:
                rotation = [0, 0, 0]
            if scale is None:
                scale = [1, 1, 1]
            
            # Generate names if not provided
            if actor_name is None:
                actor_name = f"{actor_type}_{location[0]}_{location[1]}_{location[2]}"
            
            if use_blueprint:
                if blueprint_name is None:
                    blueprint_name = f"BP_{actor_type}"
                
                # Create the Blueprint
                blueprint_params = {
                    "blueprint_name": blueprint_name,
                    "parent_class": "/Script/Engine.Actor",
                    "save_path": "/Game/Blueprints"
                }
                
                blueprint_response = unreal.send_command("create_blueprint_class", blueprint_params)
                
                if not blueprint_response or blueprint_response.get("status") != "success":
                    logger.error(f"Failed to create Blueprint: {blueprint_response}")
                    return {"success": False, "message": f"Failed to create Blueprint: {blueprint_response.get('error', 'Unknown error')}"}
                
                # Add a static mesh component
                component_params = {
                    "blueprint_name": blueprint_name,
                    "component_type": "StaticMeshComponent",
                    "component_name": f"{actor_type}Mesh"
                }
                
                component_response = unreal.send_command("add_component_to_blueprint", component_params)
                
                if not component_response or component_response.get("status") != "success":
                    logger.error(f"Failed to add component: {component_response}")
                    return {"success": False, "message": f"Failed to add component: {component_response.get('error', 'Unknown error')}"}
                
                # Set the static mesh based on actor type
                mesh_path = ""
                if actor_type.lower() == "cube":
                    mesh_path = "/Engine/BasicShapes/Cube.Cube"
                elif actor_type.lower() == "sphere":
                    mesh_path = "/Engine/BasicShapes/Sphere.Sphere"
                elif actor_type.lower() == "cylinder":
                    mesh_path = "/Engine/BasicShapes/Cylinder.Cylinder"
                elif actor_type.lower() == "cone":
                    mesh_path = "/Engine/BasicShapes/Cone.Cone"
                else:
                    mesh_path = "/Engine/BasicShapes/Cube.Cube"  # Default to cube
                
                mesh_params = {
                    "blueprint_name": blueprint_name,
                    "component_name": f"{actor_type}Mesh",
                    "static_mesh": mesh_path
                }
                
                mesh_response = unreal.send_command("set_static_mesh_properties", mesh_params)
                
                if not mesh_response or mesh_response.get("status") != "success":
                    logger.error(f"Failed to set static mesh: {mesh_response}")
                    return {"success": False, "message": f"Failed to set static mesh: {mesh_response.get('error', 'Unknown error')}"}
                
                # Compile the Blueprint
                compile_params = {
                    "blueprint_name": blueprint_name
                }
                
                compile_response = unreal.send_command("compile_blueprint", compile_params)
                
                if not compile_response or compile_response.get("status") != "success":
                    logger.error(f"Failed to compile Blueprint: {compile_response}")
                    return {"success": False, "message": f"Failed to compile Blueprint: {compile_response.get('error', 'Unknown error')}"}
                
                # Spawn the actor in the level editor (not just for testing)
                spawn_params = {
                    "blueprint_name": blueprint_name,
                    "actor_name": actor_name,
                    "location": location,
                    "rotation": rotation,
                    "scale": scale
                }
                
                spawn_response = unreal.send_command("spawn_blueprint_actor", spawn_params)
                
                if not spawn_response or spawn_response.get("status") != "success":
                    logger.error(f"Failed to spawn actor: {spawn_response}")
                    return {"success": False, "message": f"Failed to spawn actor: {spawn_response.get('error', 'Unknown error')}"}
                
                actor_name = spawn_response.get("result", {}).get("actor_name", "")
                
                return {
                    "success": True,
                    "message": f"Successfully created {actor_type} at {location}",
                    "blueprint_name": blueprint_name,
                    "actor_name": actor_name,
                    "location": location,
                    "rotation": rotation,
                    "scale": scale
                }
            else:
                # Spawn a basic actor directly
                spawn_params = {
                    "name": actor_name,
                    "type": actor_type,
                    "location": location,
                    "rotation": rotation,
                    "scale": scale
                }
                
                spawn_response = unreal.send_command("spawn_actor", spawn_params)
                
                if not spawn_response or spawn_response.get("status") != "success":
                    logger.error(f"Failed to spawn actor: {spawn_response}")
                    return {"success": False, "message": f"Failed to spawn actor: {spawn_response.get('error', 'Unknown error')}"}
                
                return {
                    "success": True,
                    "message": f"Successfully created {actor_type} at {location}",
                    "actor_name": actor_name,
                    "location": location,
                    "rotation": rotation,
                    "scale": scale
                }
            
        except Exception as e:
            error_msg = f"Error creating actor: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    logger.info("Enhanced node tools registered successfully")
