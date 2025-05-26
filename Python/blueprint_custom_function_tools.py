"""
Blueprint Custom Function Tools for Unreal MCP.

This module provides tools for creating custom functions in Blueprints
and implementing procedural logic like maze generation.
"""

import logging
import os
import json
from typing import Dict, List, Any, Optional, Tuple
from mcp.server.fastmcp import FastMCP, Context

# Get logger
logger = logging.getLogger("UnrealMCP")

def register_blueprint_custom_function_tools(mcp: FastMCP):
    """Register Blueprint custom function tools with the MCP server."""
    
    @mcp.tool()
    def create_blueprint_custom_function(
        ctx: Context,
        blueprint_name: str,
        function_name: str,
        inputs: List[Dict[str, Any]] = None,
        outputs: List[Dict[str, Any]] = None,
        pure: bool = False,
        description: str = ""
    ) -> Dict[str, Any]:
        """
        Create a custom function in a Blueprint.
        
        Args:
            blueprint_name: Name of the target Blueprint
            function_name: Name of the function to create
            inputs: List of input parameters, each a dict with 'name', 'type', and optional 'default_value'
            outputs: List of output parameters, each a dict with 'name' and 'type'
            pure: Whether the function is pure (no side effects)
            description: Description of the function
            
        Returns:
            Dict containing success status and function details
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            # Default values
            if inputs is None:
                inputs = []
            if outputs is None:
                outputs = []
            
            # Create the function
            function_params = {
                "blueprint_name": blueprint_name,
                "function_name": function_name,
                "inputs": inputs,
                "outputs": outputs,
                "pure": pure,
                "description": description
            }
            
            function_response = unreal.send_command("create_blueprint_function", function_params)
            
            if not function_response or function_response.get("status") != "success":
                logger.error(f"Failed to create function: {function_response}")
                return {"success": False, "message": f"Failed to create function: {function_response.get('error', 'Unknown error')}"}
            
            return {
                "success": True,
                "message": f"Successfully created function {function_name} in {blueprint_name}",
                "blueprint_name": blueprint_name,
                "function_name": function_name,
                "function_id": function_response.get("result", {}).get("function_id", "")
            }
            
        except Exception as e:
            error_msg = f"Error creating custom function: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    @mcp.tool()
    def implement_maze_generation_function(
        ctx: Context,
        blueprint_name: str,
        function_name: str = "GenerateMaze",
        maze_width: int = 10,
        maze_height: int = 10,
        wall_scale: float = 100.0,
        wall_height: float = 200.0,
        cube_mesh_variable: str = "WallMesh",
        material_variable: str = "WallMaterial"
    ) -> Dict[str, Any]:
        """
        Implement a maze generation function in a Blueprint using Depth-First Search algorithm.
        
        Args:
            blueprint_name: Name of the target Blueprint
            function_name: Name of the function to create or use
            maze_width: Width of the maze in cells
            maze_height: Height of the maze in cells
            wall_scale: Scale of each wall cube
            wall_height: Height of the walls
            cube_mesh_variable: Name of the variable containing the wall mesh
            material_variable: Name of the variable containing the wall material
            
        Returns:
            Dict containing success status and function details
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            # 1. Create the function if it doesn't exist
            function_params = {
                "blueprint_name": blueprint_name,
                "function_name": function_name,
                "inputs": [],
                "outputs": [],
                "pure": False,
                "description": "Generates a random maze using Depth-First Search algorithm"
            }
            
            function_response = unreal.send_command("create_blueprint_function", function_params)
            
            if not function_response or function_response.get("status") != "success":
                logger.error(f"Failed to create function: {function_response}")
                return {"success": False, "message": f"Failed to create function: {function_response.get('error', 'Unknown error')}"}
            
            function_id = function_response.get("result", {}).get("function_id", "")
            
            # 2. Create variables for maze generation
            
            # Create maze width variable
            width_var_params = {
                "blueprint_name": blueprint_name,
                "variable_name": "MazeWidth",
                "variable_type": "int",
                "default_value": str(maze_width),
                "category": "Maze Generation"
            }
            
            width_var_response = unreal.send_command("add_blueprint_variable", width_var_params)
            
            if not width_var_response or width_var_response.get("status") != "success":
                logger.error(f"Failed to create maze width variable: {width_var_response}")
                return {"success": False, "message": f"Failed to create maze width variable: {width_var_response.get('error', 'Unknown error')}"}
            
            # Create maze height variable
            height_var_params = {
                "blueprint_name": blueprint_name,
                "variable_name": "MazeHeight",
                "variable_type": "int",
                "default_value": str(maze_height),
                "category": "Maze Generation"
            }
            
            height_var_response = unreal.send_command("add_blueprint_variable", height_var_params)
            
            if not height_var_response or height_var_response.get("status") != "success":
                logger.error(f"Failed to create maze height variable: {height_var_response}")
                return {"success": False, "message": f"Failed to create maze height variable: {height_var_response.get('error', 'Unknown error')}"}
            
            # Create wall scale variable
            scale_var_params = {
                "blueprint_name": blueprint_name,
                "variable_name": "WallScale",
                "variable_type": "float",
                "default_value": str(wall_scale),
                "category": "Maze Generation"
            }
            
            scale_var_response = unreal.send_command("add_blueprint_variable", scale_var_params)
            
            if not scale_var_response or scale_var_response.get("status") != "success":
                logger.error(f"Failed to create wall scale variable: {scale_var_response}")
                return {"success": False, "message": f"Failed to create wall scale variable: {scale_var_response.get('error', 'Unknown error')}"}
            
            # Create wall height variable
            height_var_params = {
                "blueprint_name": blueprint_name,
                "variable_name": "WallHeight",
                "variable_type": "float",
                "default_value": str(wall_height),
                "category": "Maze Generation"
            }
            
            height_var_response = unreal.send_command("add_blueprint_variable", height_var_params)
            
            if not height_var_response or height_var_response.get("status") != "success":
                logger.error(f"Failed to create wall height variable: {height_var_response}")
                return {"success": False, "message": f"Failed to create wall height variable: {height_var_response.get('error', 'Unknown error')}"}
            
            # Create maze grid variable (2D array of booleans)
            grid_var_params = {
                "blueprint_name": blueprint_name,
                "variable_name": "MazeGrid",
                "variable_type": "TArray<TArray<bool>>",
                "category": "Maze Generation"
            }
            
            grid_var_response = unreal.send_command("add_blueprint_variable", grid_var_params)
            
            if not grid_var_response or grid_var_response.get("status") != "success":
                logger.error(f"Failed to create maze grid variable: {grid_var_response}")
                return {"success": False, "message": f"Failed to create maze grid variable: {grid_var_response.get('error', 'Unknown error')}"}
            
            # 3. Implement the maze generation algorithm
            
            # 3.1 Add local variables for maze generation
            
            # Add a comment node for initialization
            init_comment_params = {
                "blueprint_name": blueprint_name,
                "function_id": function_id,
                "comment": "Initialize Maze Grid",
                "position": [0, 0],
                "size": [400, 100]
            }
            
            init_comment_response = unreal.send_command("add_blueprint_comment_node", init_comment_params)
            
            # Add a comment node for DFS algorithm
            dfs_comment_params = {
                "blueprint_name": blueprint_name,
                "function_id": function_id,
                "comment": "Depth-First Search Maze Generation",
                "position": [0, 200],
                "size": [400, 100]
            }
            
            dfs_comment_response = unreal.send_command("add_blueprint_comment_node", dfs_comment_params)
            
            # Add a comment node for wall creation
            wall_comment_params = {
                "blueprint_name": blueprint_name,
                "function_id": function_id,
                "comment": "Create Wall Cubes",
                "position": [0, 400],
                "size": [400, 100]
            }
            
            wall_comment_response = unreal.send_command("add_blueprint_comment_node", wall_comment_params)
            
            # 3.2 Initialize the maze grid
            
            # Get maze width variable
            get_width_params = {
                "blueprint_name": blueprint_name,
                "function_id": function_id,
                "variable_name": "MazeWidth",
                "position": [100, 50]
            }
            
            get_width_response = unreal.send_command("add_blueprint_variable_get_node", get_width_params)
            
            if not get_width_response or get_width_response.get("status") != "success":
                logger.error(f"Failed to add get width node: {get_width_response}")
                return {"success": False, "message": f"Failed to add get width node: {get_width_response.get('error', 'Unknown error')}"}
            
            get_width_node_id = get_width_response.get("result", {}).get("node_id", "")
            
            # Get maze height variable
            get_height_params = {
                "blueprint_name": blueprint_name,
                "function_id": function_id,
                "variable_name": "MazeHeight",
                "position": [100, 100]
            }
            
            get_height_response = unreal.send_command("add_blueprint_variable_get_node", get_height_params)
            
            if not get_height_response or get_height_response.get("status") != "success":
                logger.error(f"Failed to add get height node: {get_height_response}")
                return {"success": False, "message": f"Failed to add get height node: {get_height_response.get('error', 'Unknown error')}"}
            
            get_height_node_id = get_height_response.get("result", {}).get("node_id", "")
            
            # Add a for loop for initializing the grid
            for_loop_params = {
                "blueprint_name": blueprint_name,
                "function_id": function_id,
                "loop_type": "ForLoop",
                "position": [300, 50]
            }
            
            for_loop_response = unreal.send_command("add_blueprint_loop_node", for_loop_params)
            
            if not for_loop_response or for_loop_response.get("status") != "success":
                logger.error(f"Failed to add for loop node: {for_loop_response}")
                return {"success": False, "message": f"Failed to add for loop node: {for_loop_response.get('error', 'Unknown error')}"}
            
            for_loop_node_id = for_loop_response.get("result", {}).get("node_id", "")
            
            # Connect width to for loop
            connect_width_loop_params = {
                "blueprint_name": blueprint_name,
                "function_id": function_id,
                "source_node_id": get_width_node_id,
                "source_pin": "ReturnValue",
                "target_node_id": for_loop_node_id,
                "target_pin": "LastIndex"
            }
            
            connect_width_loop_response = unreal.send_command("connect_blueprint_nodes", connect_width_loop_params)
            
            # 3.3 Add nodes for DFS maze generation
            
            # Add a function call to generate the maze using DFS
            dfs_function_params = {
                "blueprint_name": blueprint_name,
                "function_id": function_id,
                "function": "GenerateMazeWithDFS",
                "position": [300, 250]
            }
            
            dfs_function_response = unreal.send_command("add_blueprint_function_call_node", dfs_function_params)
            
            if not dfs_function_response or dfs_function_response.get("status") != "success":
                logger.error(f"Failed to add DFS function call: {dfs_function_response}")
                return {"success": False, "message": f"Failed to add DFS function call: {dfs_function_response.get('error', 'Unknown error')}"}
            
            dfs_function_node_id = dfs_function_response.get("result", {}).get("node_id", "")
            
            # 3.4 Add nodes for wall creation
            
            # Add a for loop for creating walls
            wall_loop_params = {
                "blueprint_name": blueprint_name,
                "function_id": function_id,
                "loop_type": "ForEachLoop",
                "array_type": "TArray<FVector>",
                "position": [300, 450]
            }
            
            wall_loop_response = unreal.send_command("add_blueprint_loop_node", wall_loop_params)
            
            if not wall_loop_response or wall_loop_response.get("status") != "success":
                logger.error(f"Failed to add wall loop node: {wall_loop_response}")
                return {"success": False, "message": f"Failed to add wall loop node: {wall_loop_response.get('error', 'Unknown error')}"}
            
            wall_loop_node_id = wall_loop_response.get("result", {}).get("node_id", "")
            
            # Add spawn actor from class node
            spawn_params = {
                "blueprint_name": blueprint_name,
                "function_id": function_id,
                "function": "SpawnActorFromClass",
                "position": [500, 450]
            }
            
            spawn_response = unreal.send_command("add_blueprint_function_call_node", spawn_params)
            
            if not spawn_response or spawn_response.get("status") != "success":
                logger.error(f"Failed to add spawn actor node: {spawn_response}")
                return {"success": False, "message": f"Failed to add spawn actor node: {spawn_response.get('error', 'Unknown error')}"}
            
            spawn_node_id = spawn_response.get("result", {}).get("node_id", "")
            
            # Get cube mesh variable
            get_mesh_params = {
                "blueprint_name": blueprint_name,
                "function_id": function_id,
                "variable_name": cube_mesh_variable,
                "position": [300, 550]
            }
            
            get_mesh_response = unreal.send_command("add_blueprint_variable_get_node", get_mesh_params)
            
            if not get_mesh_response or get_mesh_response.get("status") != "success":
                logger.error(f"Failed to add get mesh node: {get_mesh_response}")
                return {"success": False, "message": f"Failed to add get mesh node: {get_mesh_response.get('error', 'Unknown error')}"}
            
            get_mesh_node_id = get_mesh_response.get("result", {}).get("node_id", "")
            
            # Connect mesh to spawn actor
            connect_mesh_spawn_params = {
                "blueprint_name": blueprint_name,
                "function_id": function_id,
                "source_node_id": get_mesh_node_id,
                "source_pin": "ReturnValue",
                "target_node_id": spawn_node_id,
                "target_pin": "Class"
            }
            
            connect_mesh_spawn_response = unreal.send_command("connect_blueprint_nodes", connect_mesh_spawn_params)
            
            # Connect wall loop to spawn actor
            connect_loop_spawn_params = {
                "blueprint_name": blueprint_name,
                "function_id": function_id,
                "source_node_id": wall_loop_node_id,
                "source_pin": "ArrayElement",
                "target_node_id": spawn_node_id,
                "target_pin": "SpawnTransform"
            }
            
            connect_loop_spawn_response = unreal.send_command("connect_blueprint_nodes", connect_loop_spawn_params)
            
            # 4. Connect the function to BeginPlay event
            
            # Find the BeginPlay event
            begin_play_params = {
                "blueprint_name": blueprint_name,
                "event_type": "EventBeginPlay"
            }
            
            begin_play_response = unreal.send_command("add_blueprint_event_node", begin_play_params)
            
            if not begin_play_response or begin_play_response.get("status") != "success":
                logger.error(f"Failed to add BeginPlay event: {begin_play_response}")
                return {"success": False, "message": f"Failed to add BeginPlay event: {begin_play_response.get('error', 'Unknown error')}"}
            
            begin_play_node_id = begin_play_response.get("result", {}).get("node_id", "")
            
            # Add a function call to the maze generation function
            call_maze_params = {
                "blueprint_name": blueprint_name,
                "function": function_name,
                "position": [300, 0]
            }
            
            call_maze_response = unreal.send_command("add_blueprint_function_call_node", call_maze_params)
            
            if not call_maze_response or call_maze_response.get("status") != "success":
                logger.error(f"Failed to add function call node: {call_maze_response}")
                return {"success": False, "message": f"Failed to add function call node: {call_maze_response.get('error', 'Unknown error')}"}
            
            call_maze_node_id = call_maze_response.get("result", {}).get("node_id", "")
            
            # Connect BeginPlay to function call
            connect_begin_call_params = {
                "blueprint_name": blueprint_name,
                "source_node_id": begin_play_node_id,
                "source_pin": "ExecutionOutput",
                "target_node_id": call_maze_node_id,
                "target_pin": "ExecutionInput"
            }
            
            connect_begin_call_response = unreal.send_command("connect_blueprint_nodes", connect_begin_call_params)
            
            if not connect_begin_call_response or connect_begin_call_response.get("status") != "success":
                logger.error(f"Failed to connect BeginPlay to function call: {connect_begin_call_response}")
                return {"success": False, "message": f"Failed to connect BeginPlay to function call: {connect_begin_call_response.get('error', 'Unknown error')}"}
            
            # 5. Compile the Blueprint
            compile_params = {
                "blueprint_name": blueprint_name
            }
            
            compile_response = unreal.send_command("compile_blueprint", compile_params)
            
            if not compile_response or compile_response.get("status") != "success":
                logger.error(f"Failed to compile Blueprint: {compile_response}")
                return {"success": False, "message": f"Failed to compile Blueprint: {compile_response.get('error', 'Unknown error')}"}
            
            return {
                "success": True,
                "message": f"Successfully implemented maze generation function {function_name} in {blueprint_name}",
                "blueprint_name": blueprint_name,
                "function_name": function_name,
                "maze_width": maze_width,
                "maze_height": maze_height,
                "wall_scale": wall_scale,
                "wall_height": wall_height
            }
            
        except Exception as e:
            error_msg = f"Error implementing maze generation function: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    @mcp.tool()
    def create_dfs_helper_function(
        ctx: Context,
        blueprint_name: str,
        function_name: str = "GenerateMazeWithDFS"
    ) -> Dict[str, Any]:
        """
        Create a helper function for DFS maze generation algorithm.
        
        Args:
            blueprint_name: Name of the target Blueprint
            function_name: Name of the helper function to create
            
        Returns:
            Dict containing success status and function details
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            # 1. Create the function
            function_params = {
                "blueprint_name": blueprint_name,
                "function_name": function_name,
                "inputs": [
                    {"name": "StartX", "type": "int"},
                    {"name": "StartY", "type": "int"}
                ],
                "outputs": [],
                "pure": False,
                "description": "Helper function for DFS maze generation"
            }
            
            function_response = unreal.send_command("create_blueprint_function", function_params)
            
            if not function_response or function_response.get("status") != "success":
                logger.error(f"Failed to create function: {function_response}")
                return {"success": False, "message": f"Failed to create function: {function_response.get('error', 'Unknown error')}"}
            
            function_id = function_response.get("result", {}).get("function_id", "")
            
            # 2. Add local variables for DFS
            
            # Add a comment node for DFS algorithm
            dfs_comment_params = {
                "blueprint_name": blueprint_name,
                "function_id": function_id,
                "comment": "DFS Maze Generation Algorithm",
                "position": [0, 0],
                "size": [400, 100]
            }
            
            dfs_comment_response = unreal.send_command("add_blueprint_comment_node", dfs_comment_params)
            
            # Add a local variable for visited cells
            visited_var_params = {
                "blueprint_name": blueprint_name,
                "function_id": function_id,
                "variable_name": "Visited",
                "variable_type": "TArray<TArray<bool>>",
                "is_local": True
            }
            
            visited_var_response = unreal.send_command("add_blueprint_variable", visited_var_params)
            
            if not visited_var_response or visited_var_response.get("status") != "success":
                logger.error(f"Failed to create visited variable: {visited_var_response}")
                return {"success": False, "message": f"Failed to create visited variable: {visited_var_response.get('error', 'Unknown error')}"}
            
            # Add a local variable for directions
            directions_var_params = {
                "blueprint_name": blueprint_name,
                "function_id": function_id,
                "variable_name": "Directions",
                "variable_type": "TArray<FVector2D>",
                "is_local": True
            }
            
            directions_var_response = unreal.send_command("add_blueprint_variable", directions_var_params)
            
            if not directions_var_response or directions_var_response.get("status") != "success":
                logger.error(f"Failed to create directions variable: {directions_var_response}")
                return {"success": False, "message": f"Failed to create directions variable: {directions_var_response.get('error', 'Unknown error')}"}
            
            # 3. Implement the DFS algorithm
            
            # Add a recursive function call
            recursive_call_params = {
                "blueprint_name": blueprint_name,
                "function_id": function_id,
                "function": function_name,
                "position": [500, 300]
            }
            
            recursive_call_response = unreal.send_command("add_blueprint_function_call_node", recursive_call_params)
            
            if not recursive_call_response or recursive_call_response.get("status") != "success":
                logger.error(f"Failed to add recursive function call: {recursive_call_response}")
                return {"success": False, "message": f"Failed to add recursive function call: {recursive_call_response.get('error', 'Unknown error')}"}
            
            # 4. Compile the Blueprint
            compile_params = {
                "blueprint_name": blueprint_name
            }
            
            compile_response = unreal.send_command("compile_blueprint", compile_params)
            
            if not compile_response or compile_response.get("status") != "success":
                logger.error(f"Failed to compile Blueprint: {compile_response}")
                return {"success": False, "message": f"Failed to compile Blueprint: {compile_response.get('error', 'Unknown error')}"}
            
            return {
                "success": True,
                "message": f"Successfully created DFS helper function {function_name} in {blueprint_name}",
                "blueprint_name": blueprint_name,
                "function_name": function_name
            }
            
        except Exception as e:
            error_msg = f"Error creating DFS helper function: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    @mcp.tool()
    def connect_blueprint_function_to_event(
        ctx: Context,
        blueprint_name: str,
        function_name: str,
        event_type: str = "EventBeginPlay"
    ) -> Dict[str, Any]:
        """
        Connect a Blueprint function to an event.
        
        Args:
            blueprint_name: Name of the target Blueprint
            function_name: Name of the function to connect
            event_type: Type of event to connect to
            
        Returns:
            Dict containing success status and connection details
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            # 1. Find or create the event
            event_params = {
                "blueprint_name": blueprint_name,
                "event_type": event_type
            }
            
            event_response = unreal.send_command("add_blueprint_event_node", event_params)
            
            if not event_response or event_response.get("status") != "success":
                logger.error(f"Failed to add event node: {event_response}")
                return {"success": False, "message": f"Failed to add event node: {event_response.get('error', 'Unknown error')}"}
            
            event_node_id = event_response.get("result", {}).get("node_id", "")
            
            # 2. Add a function call to the function
            call_params = {
                "blueprint_name": blueprint_name,
                "function": function_name,
                "position": [300, 0]
            }
            
            call_response = unreal.send_command("add_blueprint_function_call_node", call_params)
            
            if not call_response or call_response.get("status") != "success":
                logger.error(f"Failed to add function call node: {call_response}")
                return {"success": False, "message": f"Failed to add function call node: {call_response.get('error', 'Unknown error')}"}
            
            call_node_id = call_response.get("result", {}).get("node_id", "")
            
            # 3. Connect the event to the function call
            connect_params = {
                "blueprint_name": blueprint_name,
                "source_node_id": event_node_id,
                "source_pin": "ExecutionOutput",
                "target_node_id": call_node_id,
                "target_pin": "ExecutionInput"
            }
            
            connect_response = unreal.send_command("connect_blueprint_nodes", connect_params)
            
            if not connect_response or connect_response.get("status") != "success":
                logger.error(f"Failed to connect event to function call: {connect_response}")
                return {"success": False, "message": f"Failed to connect event to function call: {connect_response.get('error', 'Unknown error')}"}
            
            # 4. Compile the Blueprint
            compile_params = {
                "blueprint_name": blueprint_name
            }
            
            compile_response = unreal.send_command("compile_blueprint", compile_params)
            
            if not compile_response or compile_response.get("status") != "success":
                logger.error(f"Failed to compile Blueprint: {compile_response}")
                return {"success": False, "message": f"Failed to compile Blueprint: {compile_response.get('error', 'Unknown error')}"}
            
            return {
                "success": True,
                "message": f"Successfully connected function {function_name} to {event_type} in {blueprint_name}",
                "blueprint_name": blueprint_name,
                "function_name": function_name,
                "event_type": event_type
            }
            
        except Exception as e:
            error_msg = f"Error connecting function to event: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    logger.info("Blueprint custom function tools registered successfully")
