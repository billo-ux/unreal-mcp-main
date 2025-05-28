"""
Node & Graph Tools for Unreal MCP.

This module provides tools for manipulating Blueprint nodes, graphs, and variables.
"""

import logging
from typing import Dict, List, Any, Optional
from mcp.server.fastmcp import FastMCP, Context
from unreal_mcp_server import get_unreal_connection

logger = logging.getLogger("UnrealMCP")

def register_node_graph_tools(mcp: FastMCP):
    """Register node and graph tools with the MCP server."""
    # ... (tools will be added here in subsequent steps)

    @mcp.tool()
    def add_event_node(ctx: Context, blueprint_name: str, event_name: str, node_position: List[int] = None) -> Dict[str, Any]:
        """
        Add an event node to a Blueprint's event graph.
        Args:
            blueprint_name: Name of the target Blueprint
            event_name: Name of the event (e.g., 'ReceiveBeginPlay')
            node_position: [X, Y] position in the graph (default: [0, 0])
        Returns:
            Response containing the node ID and success status
        """
        try:
            if node_position is None:
                node_position = [0, 0]
            params = {"blueprint_name": blueprint_name, "event_name": event_name, "node_position": node_position}
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            response = unreal.send_command("add_blueprint_event_node", params)
            return response or {"success": False, "message": "No response from Unreal Engine"}
        except Exception as e:
            logger.error(f"Error adding event node: {e}")
            return {"success": False, "message": str(e)}

    @mcp.tool()
    def add_input_action_node(ctx: Context, blueprint_name: str, action_name: str, node_position: List[int] = None) -> Dict[str, Any]:
        """
        Add an input action event node to a Blueprint's event graph.
        Args:
            blueprint_name: Name of the target Blueprint
            action_name: Name of the input action
            node_position: [X, Y] position in the graph (default: [0, 0])
        Returns:
            Response containing the node ID and success status
        """
        try:
            if node_position is None:
                node_position = [0, 0]
            params = {"blueprint_name": blueprint_name, "action_name": action_name, "node_position": node_position}
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            response = unreal.send_command("add_blueprint_input_action_node", params)
            return response or {"success": False, "message": "No response from Unreal Engine"}
        except Exception as e:
            logger.error(f"Error adding input action node: {e}")
            return {"success": False, "message": str(e)}

    @mcp.tool()
    def add_function_node(ctx: Context, blueprint_name: str, target: str, function_name: str, params_dict: Dict[str, Any] = None, node_position: List[int] = None) -> Dict[str, Any]:
        """
        Add a function call node to a Blueprint's event graph.
        Args:
            blueprint_name: Name of the target Blueprint
            target: Target object for the function (component name or self)
            function_name: Name of the function to call
            params_dict: Parameters to set on the function node (default: empty dict)
            node_position: [X, Y] position in the graph (default: [0, 0])
        Returns:
            Response containing the node ID and success status
        """
        try:
            if params_dict is None:
                params_dict = {}
            if node_position is None:
                node_position = [0, 0]
            command_params = {"blueprint_name": blueprint_name, "target": target, "function_name": function_name, "params": params_dict, "node_position": node_position}
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            response = unreal.send_command("add_blueprint_function_node", command_params)
            return response or {"success": False, "message": "No response from Unreal Engine"}
        except Exception as e:
            logger.error(f"Error adding function node: {e}")
            return {"success": False, "message": str(e)}

    @mcp.tool()
    def connect_nodes(ctx: Context, blueprint_name: str, source_node_id: str, source_pin: str, target_node_id: str, target_pin: str) -> Dict[str, Any]:
        """
        Connect two nodes in a Blueprint's event graph.
        Args:
            blueprint_name: Name of the target Blueprint
            source_node_id: ID of the source node
            source_pin: Name of the output pin on the source node
            target_node_id: ID of the target node
            target_pin: Name of the input pin on the target node
        Returns:
            Response indicating success or failure
        """
        try:
            params = {"blueprint_name": blueprint_name, "source_node_id": source_node_id, "source_pin": source_pin, "target_node_id": target_node_id, "target_pin": target_pin}
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            response = unreal.send_command("connect_blueprint_nodes", params)
            return response or {"success": False, "message": "No response from Unreal Engine"}
        except Exception as e:
            logger.error(f"Error connecting nodes: {e}")
            return {"success": False, "message": str(e)}

    @mcp.tool()
    def add_variable(ctx: Context, blueprint_name: str, variable_name: str, variable_type: str, is_exposed: bool = False) -> Dict[str, Any]:
        """
        Add a variable to a Blueprint.
        Args:
            blueprint_name: Name of the target Blueprint
            variable_name: Name of the variable
            variable_type: Type of the variable (Boolean, Integer, Float, Vector, etc.)
            is_exposed: Whether to expose the variable to the editor
        Returns:
            Response indicating success or failure
        """
        try:
            params = {"blueprint_name": blueprint_name, "variable_name": variable_name, "variable_type": variable_type, "is_exposed": is_exposed}
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            response = unreal.send_command("add_blueprint_variable", params)
            return response or {"success": False, "message": "No response from Unreal Engine"}
        except Exception as e:
            logger.error(f"Error adding variable: {e}")
            return {"success": False, "message": str(e)}

    @mcp.tool()
    def get_node_properties(ctx: Context, blueprint_name: str, node_id: str) -> Dict[str, Any]:
        """
        Get properties of a node in a Blueprint's event graph.
        Args:
            blueprint_name: Name of the target Blueprint
            node_id: ID of the node
        Returns:
            Dict of node properties
        """
        try:
            params = {"blueprint_name": blueprint_name, "node_id": node_id}
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            response = unreal.send_command("get_node_properties", params)
            return response or {"success": False, "message": "No response from Unreal Engine"}
        except Exception as e:
            logger.error(f"Error getting node properties: {e}")
            return {"success": False, "message": str(e)}

    @mcp.tool()
    def set_node_property(ctx: Context, blueprint_name: str, node_id: str, property_name: str, property_value) -> Dict[str, Any]:
        """
        Set a property on a node in a Blueprint's event graph.
        Args:
            blueprint_name: Name of the target Blueprint
            node_id: ID of the node
            property_name: Name of the property to set
            property_value: Value to set the property to
        Returns:
            Response indicating success or failure
        """
        try:
            params = {"blueprint_name": blueprint_name, "node_id": node_id, "property_name": property_name, "property_value": property_value}
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            response = unreal.send_command("set_node_property", params)
            return response or {"success": False, "message": "No response from Unreal Engine"}
        except Exception as e:
            logger.error(f"Error setting node property: {e}")
            return {"success": False, "message": str(e)}

    @mcp.tool()
    def delete_node(ctx: Context, blueprint_name: str, node_id: str) -> Dict[str, Any]:
        """
        Delete a node from a Blueprint's event graph.
        Args:
            blueprint_name: Name of the target Blueprint
            node_id: ID of the node to delete
        Returns:
            Response indicating success or failure
        """
        try:
            params = {"blueprint_name": blueprint_name, "node_id": node_id}
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            response = unreal.send_command("delete_node", params)
            return response or {"success": False, "message": "No response from Unreal Engine"}
        except Exception as e:
            logger.error(f"Error deleting node: {e}")
            return {"success": False, "message": str(e)}

    @mcp.tool()
    def find_nodes(ctx: Context, blueprint_name: str, node_type: str = None, event_type: str = None) -> Dict[str, Any]:
        """
        Find nodes in a Blueprint's event graph.
        Args:
            blueprint_name: Name of the target Blueprint
            node_type: Type of node to find (Event, Function, Variable, etc.)
            event_type: Specific event type to find (BeginPlay, Tick, etc.)
        Returns:
            Dict containing array of found node IDs and success status
        """
        try:
            params = {"blueprint_name": blueprint_name}
            if node_type is not None:
                params["node_type"] = node_type
            if event_type is not None:
                params["event_type"] = event_type
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            response = unreal.send_command("find_blueprint_nodes", params)
            return response or {"success": False, "message": "No response from Unreal Engine"}
        except Exception as e:
            logger.error(f"Error finding nodes: {e}")
            return {"success": False, "message": str(e)} 