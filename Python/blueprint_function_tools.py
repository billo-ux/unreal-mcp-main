"""
Blueprint Function Tools for Unreal MCP.

This module provides tools for generating Blueprint functions using AI.
"""

import logging
import json
import os
from typing import Dict, List, Any, Optional
from mcp.server.fastmcp import FastMCP, Context

# Get logger
logger = logging.getLogger("UnrealMCP")

# Import AI service
from ai_service import AIService, AIServiceConfig

# Load AI service configuration
config = AIServiceConfig()
config_file = os.path.expanduser("~/.unreal_mcp/ai_config.json")
if os.path.exists(config_file):
    config.load_from_file(config_file)
else:
    # Create default config
    config.save_to_file(config_file)

# Create AI service
ai_service = AIService(config)

def register_blueprint_function_tools(mcp: FastMCP):
    """Register Blueprint function tools with the MCP server."""
    
    @mcp.tool()
    def generate_blueprint_function(
        ctx: Context,
        blueprint_name: str,
        function_description: str,
        get_blueprint_context: bool = True
    ) -> Dict[str, Any]:
        """
        Generate a Blueprint function using AI.
        
        Args:
            blueprint_name: Name of the target Blueprint
            function_description: Natural language description of the function
            get_blueprint_context: Whether to get the Blueprint context for better generation
            
        Returns:
            Dict containing the generated function details and success status
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            # Get Blueprint context if requested
            blueprint_context = None
            if get_blueprint_context:
                blueprint_context = _get_blueprint_context(unreal, blueprint_name)
            
            # Generate function using AI
            function_data = ai_service.generate_blueprint_function(
                function_description,
                blueprint_context
            )
            
            if not function_data:
                logger.error("Failed to generate Blueprint function")
                return {"success": False, "message": "Failed to generate Blueprint function"}
            
            # Create required structs if any
            if 'required_structs' in function_data and function_data['required_structs']:
                for struct_data in function_data['required_structs']:
                    _create_struct(unreal, struct_data)
            
            # Create required enums if any
            if 'required_enums' in function_data and function_data['required_enums']:
                for enum_data in function_data['required_enums']:
                    _create_enum(unreal, enum_data)
            
            # Create the function in the Blueprint
            result = _create_function_in_blueprint(unreal, blueprint_name, function_data)
            
            if not result:
                logger.error("Failed to create function in Blueprint")
                return {"success": False, "message": "Failed to create function in Blueprint"}
            
            # Compile the Blueprint
            compile_params = {
                "blueprint_name": blueprint_name
            }
            
            compile_response = unreal.send_command("compile_blueprint", compile_params)
            
            if not compile_response or compile_response.get("status") != "success":
                logger.error(f"Failed to compile Blueprint: {compile_response}")
                return {"success": False, "message": "Failed to compile Blueprint"}
            
            return {
                "success": True,
                "message": f"Successfully generated function '{function_data['function_name']}'",
                "function_name": function_data['function_name'],
                "function_data": function_data
            }
            
        except Exception as e:
            error_msg = f"Error generating Blueprint function: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    @mcp.tool()
    def configure_ai_service(
        ctx: Context,
        openai_api_key: str = None,
        gemini_api_key: str = None,
        local_agent_url: str = None,
        selected_service: str = None
    ) -> Dict[str, Any]:
        """
        Configure the AI service.
        
        Args:
            openai_api_key: OpenAI API key
            gemini_api_key: Google Gemini API key
            local_agent_url: URL for local LLM agent
            selected_service: Selected AI service ("openai", "gemini", or "local")
            
        Returns:
            Dict containing success status and configuration details
        """
        try:
            # Update configuration
            if openai_api_key is not None:
                config.openai_api_key = openai_api_key
            if gemini_api_key is not None:
                config.gemini_api_key = gemini_api_key
            if local_agent_url is not None:
                config.local_agent_url = local_agent_url
            if selected_service is not None:
                if selected_service not in ["openai", "gemini", "local"]:
                    return {"success": False, "message": "Invalid service selection. Must be 'openai', 'gemini', or 'local'."}
                config.selected_service = selected_service
            
            # Save configuration
            config_file = os.path.expanduser("~/.unreal_mcp/ai_config.json")
            if not config.save_to_file(config_file):
                return {"success": False, "message": "Failed to save configuration"}
            
            return {
                "success": True,
                "message": "AI service configuration updated",
                "selected_service": config.selected_service,
                "openai_configured": bool(config.openai_api_key),
                "gemini_configured": bool(config.gemini_api_key),
                "local_agent_configured": bool(config.local_agent_url)
            }
            
        except Exception as e:
            error_msg = f"Error configuring AI service: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    logger.info("Blueprint function tools registered successfully")

def _get_blueprint_context(unreal, blueprint_name: str) -> Dict[str, Any]:
    """Get context information about a Blueprint for better function generation."""
    context = {
        "variables": [],
        "functions": [],
        "components": []
    }
    
    try:
        # Get Blueprint variables
        var_params = {
            "blueprint_name": blueprint_name
        }
        
        var_response = unreal.send_command("get_blueprint_variables", var_params)
        
        if var_response and var_response.get("status") == "success":
            variables = var_response.get("result", {}).get("variables", [])
            context["variables"] = variables
        
        # Get Blueprint functions
        func_params = {
            "blueprint_name": blueprint_name
        }
        
        func_response = unreal.send_command("get_blueprint_functions", func_params)
        
        if func_response and func_response.get("status") == "success":
            functions = func_response.get("result", {}).get("functions", [])
            context["functions"] = functions
        
        # Get Blueprint components
        comp_params = {
            "blueprint_name": blueprint_name
        }
        
        comp_response = unreal.send_command("get_blueprint_components", comp_params)
        
        if comp_response and comp_response.get("status") == "success":
            components = comp_response.get("result", {}).get("components", [])
            context["components"] = components
        
        return context
        
    except Exception as e:
        logger.error(f"Error getting Blueprint context: {e}")
        return context

def _create_struct(unreal, struct_data: Dict[str, Any]) -> bool:
    """Create a struct in Unreal Engine."""
    try:
        struct_params = {
            "struct_name": struct_data["name"],
            "properties": struct_data["properties"]
        }
        
        response = unreal.send_command("create_struct", struct_params)
        
        if not response or response.get("status") != "success":
            logger.error(f"Failed to create struct: {response}")
            return False
        
        return True
        
    except Exception as e:
        logger.error(f"Error creating struct: {e}")
        return False

def _create_enum(unreal, enum_data: Dict[str, Any]) -> bool:
    """Create an enum in Unreal Engine."""
    try:
        enum_params = {
            "enum_name": enum_data["name"],
            "values": enum_data["values"]
        }
        
        response = unreal.send_command("create_enum", enum_params)
        
        if not response or response.get("status") != "success":
            logger.error(f"Failed to create enum: {response}")
            return False
        
        return True
        
    except Exception as e:
        logger.error(f"Error creating enum: {e}")
        return False

def _create_function_in_blueprint(unreal, blueprint_name: str, function_data: Dict[str, Any]) -> bool:
    """Create a function in a Blueprint based on the generated data."""
    try:
        # Create the function
        function_params = {
            "blueprint_name": blueprint_name,
            "function_name": function_data["function_name"],
            "return_type": function_data.get("return_type", "None")
        }
        
        # Add parameters if any
        if "parameters" in function_data and function_data["parameters"]:
            function_params["parameters"] = function_data["parameters"]
        
        response = unreal.send_command("create_blueprint_function", function_params)
        
        if not response or response.get("status") != "success":
            logger.error(f"Failed to create function: {response}")
            return False
        
        # Create local variables if any
        if "local_variables" in function_data and function_data["local_variables"]:
            for var in function_data["local_variables"]:
                var_params = {
                    "blueprint_name": blueprint_name,
                    "function_name": function_data["function_name"],
                    "variable_name": var["name"],
                    "variable_type": var["type"]
                }
                
                var_response = unreal.send_command("add_local_variable", var_params)
                
                if not var_response or var_response.get("status") != "success":
                    logger.warning(f"Failed to create local variable: {var_response}")
        
        # Create nodes
        node_id_map = {}  # Map AI-generated node IDs to actual node IDs
        
        for node in function_data["nodes"]:
            node_params = {
                "blueprint_name": blueprint_name,
                "function_name": function_data["function_name"],
                "node_type": node["type"],
                "position": node.get("position", [0, 0])
            }
            
            # Add node-specific parameters
            if node["type"] == "FunctionCall":
                node_params["function"] = node["function"]
                node_params["target"] = node.get("target", "self")
                if "parameters" in node:
                    node_params["parameters"] = node["parameters"]
            
            node_response = unreal.send_command("add_blueprint_node", node_params)
            
            if not node_response or node_response.get("status") != "success":
                logger.warning(f"Failed to create node: {node_response}")
                continue
            
            # Store the mapping from AI node ID to actual node ID
            actual_node_id = node_response.get("result", {}).get("node_id")
            if actual_node_id:
                node_id_map[node["id"]] = actual_node_id
        
        # Create connections
        for connection in function_data["connections"]:
            # Skip if we don't have the node IDs
            if connection["from_node"] not in node_id_map or connection["to_node"] not in node_id_map:
                logger.warning(f"Skipping connection due to missing node: {connection}")
                continue
            
            connection_params = {
                "blueprint_name": blueprint_name,
                "function_name": function_data["function_name"],
                "source_node_id": node_id_map[connection["from_node"]],
                "source_pin": connection["from_pin"],
                "target_node_id": node_id_map[connection["to_node"]],
                "target_pin": connection["to_pin"]
            }
            
            connection_response = unreal.send_command("connect_blueprint_nodes", connection_params)
            
            if not connection_response or connection_response.get("status") != "success":
                logger.warning(f"Failed to create connection: {connection_response}")
        
        return True
        
    except Exception as e:
        logger.error(f"Error creating function in Blueprint: {e}")
        return False

@mcp.tool()
def set_skeletal_mesh_component(
    ctx: Context,
    blueprint_name: str,
    component_name: str,
    skeletal_mesh_path: str
) -> Dict[str, Any]:
    """Set a skeletal mesh for a component."""
    unreal = get_unreal_connection()
    if not unreal:
        return {"success": False, "message": "Failed to connect to Unreal Engine"}
    
    params = {
        "blueprint_name": blueprint_name,
        "component_name": component_name,
        "skeletal_mesh_path": skeletal_mesh_path
    }
    
    response = unreal.send_command("set_skeletal_mesh", params)
    return response

@mcp.tool()
def attach_component(
    ctx: Context,
    blueprint_name: str,
    component_name: str,
    parent_component_name: str,
    socket_name: str = ""
) -> Dict[str, Any]:
    """Attach a component to another component."""
    unreal = get_unreal_connection()
    if not unreal:
        return {"success": False, "message": "Failed to connect to Unreal Engine"}
    
    params = {
        "blueprint_name": blueprint_name,
        "component_name": component_name,
        "parent_component_name": parent_component_name,
        "socket_name": socket_name
    }
    
    response = unreal.send_command("attach_component", params)
    return response
