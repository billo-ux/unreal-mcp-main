"""
Unreal Engine MCP Server

A simple MCP server for interacting with Unreal Engine.
"""
import logging
import socket
import sys
import os
import json
from contextlib import asynccontextmanager
from typing import AsyncIterator, Dict, Any, Optional
from mcp.server.fastmcp import FastMCP
from enhanced_node_tools import register_enhanced_node_tools
from blueprint_custom_function_tools import register_blueprint_custom_function_tools


# Add the current directory to the path to import the new modules
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# Import new modules
from ai_service import AIService, AIServiceConfig
from http_client import HTTPClient
from blueprint_function_tools import register_blueprint_function_tools
from ui_tools import register_ui_tools
# Import the asset creation tools
from asset_creation_tools import register_asset_creation_tools

# Configure logging with more detailed format
logging.basicConfig(
    level=logging.DEBUG,  # Change to DEBUG level for more details
    format='%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
    handlers=[
        logging.FileHandler('unreal_mcp.log'),
        # logging.StreamHandler(sys.stdout) # Remove this handler to unexpected non-whitespace characters in JSON
    ]
)
logger = logging.getLogger("UnrealMCP")

# Configuration
UNREAL_HOST = "127.0.0.1"
UNREAL_PORT = 55557

# Function to register toolbar button
def register_toolbar_button(button_name: str, tooltip: str, icon_path: str = None) -> Dict[str, Any]:
    """Register a toolbar button in the Unreal Editor."""
    unreal = get_unreal_connection()
    if not unreal:
        logger.error("Failed to connect to Unreal Engine")
        return {"success": False, "message": "Failed to connect to Unreal Engine"}
        
    params = {
        "button_name": button_name,
        "tooltip": tooltip
    }
    
    if icon_path:
        params["icon_path"] = icon_path
        
    response = unreal.send_command("register_toolbar_button", params)
    
    if not response:
        logger.error("No response from Unreal Engine")
        return {"success": False, "message": "No response from Unreal Engine"}
    
    logger.info(f"Register toolbar button response: {response}")
    return response

class UnrealConnection:
    """Connection to an Unreal Engine instance."""
    
    def __init__(self):
        """Initialize the connection."""
        self.socket = None
        self.connected = False
    
    def connect(self) -> bool:
        """Connect to the Unreal Engine instance."""
        try:
            # Close any existing socket
            if self.socket:
                try:
                    self.socket.close()
                except:
                    pass
                self.socket = None
            
            logger.info(f"Connecting to Unreal at {UNREAL_HOST}:{UNREAL_PORT}...")
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(5)  # 5 second timeout
            
            # Set socket options for better stability
            self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            
            # Set larger buffer sizes
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 65536)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 65536)
            
            self.socket.connect((UNREAL_HOST, UNREAL_PORT))
            self.connected = True
            logger.info("Connected to Unreal Engine")
            return True
            
        except Exception as e:
            logger.error(f"Failed to connect to Unreal: {e}")
            self.connected = False
            return False
    
    def disconnect(self):
        """Disconnect from the Unreal Engine instance."""
        if self.socket:
            try:
                self.socket.close()
            except:
                pass
        self.socket = None
        self.connected = False

    def receive_full_response(self, sock, buffer_size=4096) -> bytes:
        """Receive a complete response from Unreal, handling chunked data."""
        chunks = []
        sock.settimeout(5)  # 5 second timeout
        try:
            while True:
                chunk = sock.recv(buffer_size)
                if not chunk:
                    if not chunks:
                        raise Exception("Connection closed before receiving data")
                    break
                chunks.append(chunk)
                
                # Process the data received so far
                data = b''.join(chunks)
                decoded_data = data.decode('utf-8')
                
                # Try to parse as JSON to check if complete
                try:
                    json.loads(decoded_data)
                    logger.info(f"Received complete response ({len(data)} bytes)")
                    return data
                except json.JSONDecodeError:
                    # Not complete JSON yet, continue reading
                    logger.debug(f"Received partial response, waiting for more data...")
                    continue
                except Exception as e:
                    logger.warning(f"Error processing response chunk: {str(e)}")
                    continue
        except socket.timeout:
            logger.warning("Socket timeout during receive")
            if chunks:
                # If we have some data already, try to use it
                data = b''.join(chunks)
                try:
                    json.loads(data.decode('utf-8'))
                    logger.info(f"Using partial response after timeout ({len(data)} bytes)")
                    return data
                except:
                    pass
            raise Exception("Timeout receiving Unreal response")
        except Exception as e:
            logger.error(f"Error during receive: {str(e)}")
            raise
    
    def send_command(self, command: str, params: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
        """Send a command to Unreal Engine and get the response."""
        # Always reconnect for each command, since Unreal closes the connection after each command
        # This is different from Unity which keeps connections alive
        if self.socket:
            try:
                self.socket.close()
            except:
                pass
            self.socket = None
            self.connected = False
        
        if not self.connect():
            logger.error("Failed to connect to Unreal Engine for command")
            return None
        
        try:
            # Match Unity's command format exactly
            command_obj = {
                "type": command,  # Use "type" instead of "command"
                "params": params or {}  # Use Unity's params or {} pattern
            }
            
            # Send without newline, exactly like Unity
            command_json = json.dumps(command_obj)
            logger.info(f"Sending command: {command_json}")
            self.socket.sendall(command_json.encode('utf-8'))
            
            # Read response using improved handler
            response_data = self.receive_full_response(self.socket)
            response = json.loads(response_data.decode('utf-8'))
            
            # Log complete response for debugging
            logger.info(f"Complete response from Unreal: {response}")
            
            # Check for both error formats: {"status": "error", ...} and {"success": false, ...}
            if response.get("status") == "error":
                error_message = response.get("error") or response.get("message", "Unknown Unreal error")
                logger.error(f"Unreal error (status=error): {error_message}")
                # We want to preserve the original error structure but ensure error is accessible
                if "error" not in response:
                    response["error"] = error_message
            elif response.get("success") is False:
                # This format uses {"success": false, "error": "message"} or {"success": false, "message": "message"}
                error_message = response.get("error") or response.get("message", "Unknown Unreal error")
                logger.error(f"Unreal error (success=false): {error_message}")
                # Convert to the standard format expected by higher layers
                response = {
                    "status": "error",
                    "error": error_message
                }
            
            # Always close the connection after command is complete
            # since Unreal will close it on its side anyway
            try:
                self.socket.close()
            except:
                pass
            self.socket = None
            self.connected = False
            
            return response
            
        except Exception as e:
            logger.error(f"Error sending command: {e}")
            # Always reset connection state on any error
            self.connected = False
            try:
                self.socket.close()
            except:
                pass
            self.socket = None
            return {
                "status": "error",
                "error": str(e)
            }

# Global connection state
_unreal_connection: UnrealConnection = None

def get_unreal_connection() -> Optional[UnrealConnection]:
    """Get the connection to Unreal Engine."""
    global _unreal_connection
    try:
        if _unreal_connection is None:
            _unreal_connection = UnrealConnection()
            if not _unreal_connection.connect():
                logger.warning("Could not connect to Unreal Engine")
                _unreal_connection = None
        else:
            # Verify connection is still valid with a ping-like test
            try:
                # Simple test by sending an empty buffer to check if socket is still connected
                _unreal_connection.socket.sendall(b'\x00')
                logger.debug("Connection verified with ping test")
            except Exception as e:
                logger.warning(f"Existing connection failed: {e}")
                _unreal_connection.disconnect()
                _unreal_connection = None
                # Try to reconnect
                _unreal_connection = UnrealConnection()
                if not _unreal_connection.connect():
                    logger.warning("Could not reconnect to Unreal Engine")
                    _unreal_connection = None
                else:
                    logger.info("Successfully reconnected to Unreal Engine")
        
        return _unreal_connection
    except Exception as e:
        logger.error(f"Error getting Unreal connection: {e}")
        return None

@asynccontextmanager
async def server_lifespan(server: FastMCP) -> AsyncIterator[Dict[str, Any]]:
    """Handle server startup and shutdown."""
    global _unreal_connection
    logger.info("UnrealMCP server starting up")
    try:
        _unreal_connection = get_unreal_connection()
        if _unreal_connection:
            logger.info("Connected to Unreal Engine on startup")
        else:
            logger.warning("Could not connect to Unreal Engine on startup")
    except Exception as e:
        logger.error(f"Error connecting to Unreal Engine on startup: {e}")
        _unreal_connection = None
    
    try:
        yield {}
    finally:
        if _unreal_connection:
            _unreal_connection.disconnect()
            _unreal_connection = None
        logger.info("Unreal MCP server shut down")

# Initialize server
mcp = FastMCP(
    "UnrealMCP",
    description="Unreal Engine integration via Model Context Protocol",
    lifespan=server_lifespan
)

# Import and register tools
from tools.editor_tools import register_editor_tools
from tools.blueprint_tools import register_blueprint_tools
from tools.node_tools import register_blueprint_node_tools
from tools.project_tools import register_project_tools
from tools.umg_tools import register_umg_tools

# Register all tools
def register_all_tools():
    # Register existing tools
    register_editor_tools(mcp)
    register_blueprint_tools(mcp)
    register_blueprint_node_tools(mcp)
    register_project_tools(mcp)
    register_umg_tools(mcp)
    register_enhanced_node_tools(mcp)
    register_asset_creation_tools(mcp)
    # Register new tools
    register_blueprint_function_tools(mcp)
    register_ui_tools(mcp)
    # Register Blueprint custom function tools
    register_blueprint_custom_function_tools(mcp)

    
    # Register toolbar button
    register_toolbar_button(
        "AI Blueprint Generator",
        "Generate Blueprint functions using AI",
        None  # No icon path for now
    )
    
    logger.info("All tools registered successfully")

# Call the function to register all tools
register_all_tools()

@mcp.prompt()
def info():
    """Information about available Unreal MCP tools and best practices."""
    return """
    # Unreal MCP Server Tools and Best Practices
    
    ## AI-Powered Blueprint Function Generation
    - `generate_blueprint_function(blueprint_name, function_description)` 
      Generate a Blueprint function using AI
    - `configure_ai_service(openai_api_key, gemini_api_key, local_agent_url, selected_service)`
      Configure the AI service
    - `show_function_generation_dialog(blueprint_name)`
      Show a dialog for generating Blueprint functions
    - `show_ai_configuration_dialog()`
      Show a dialog for configuring AI services
    
    ## UMG (Widget Blueprint) Tools
    - `create_umg_widget_blueprint(widget_name, parent_class="UserWidget", path="/Game/UI")` 
      Create a new UMG Widget Blueprint
    - `add_text_block_to_widget(widget_name, text_block_name, text="", position=[0,0], size=[200,50], font_size=12, color=[1,1,1,1])`
      Add a Text Block widget with customizable properties
    - `add_button_to_widget(widget_name, button_name, text="", position=[0,0], size=[200,50], font_size=12, color=[1,1,1,1], background_color=[0.1,0.1,0.1,1])`
      Add a Button widget with text and styling
    - `bind_widget_event(widget_name, widget_component_name, event_name, function_name="")`
      Bind events like OnClicked to functions
    - `add_widget_to_viewport(widget_name, z_order=0)`
      Add widget instance to game viewport
    - `set_text_block_binding(widget_name, text_block_name, binding_property, binding_type="Text")`
      Set up dynamic property binding for text blocks

    ## Editor Tools
    ### Viewport and Screenshots
    - `focus_viewport(target, location, distance, orientation)` - Focus viewport
    - `take_screenshot(filename, show_ui, resolution)` - Capture screenshots

    ### Actor Management
    - `get_actors_in_level()` - List all actors in current level
    - `find_actors_by_name(pattern)` - Find actors by name pattern
    - `spawn_actor(name, type, location=[0,0,0], rotation=[0,0,0], scale=[1,1,1])` - Create actors
    - `delete_actor(name)` - Remove actors
    - `set_actor_transform(name, location, rotation, scale)` - Modify actor transform
    - `get_actor_properties(name)` - Get actor properties
    
    ## Blueprint Management
    - `create_blueprint(name, parent_class)` - Create new Blueprint classes
    - `add_component_to_blueprint(blueprint_name, component_type, component_name)` - Add components
    - `set_static_mesh_properties(blueprint_name, component_name, static_mesh)` - Configure meshes
    - `set_physics_properties(blueprint_name, component_name)` - Configure physics
    - `compile_blueprint(blueprint_name)` - Compile Blueprint changes
    - `set_blueprint_property(blueprint_name, property_name, property_value)` - Set properties
    - `set_pawn_properties(blueprint_name)` - Configure Pawn settings
    - `spawn_blueprint_actor(blueprint_name, actor_name)` - Spawn Blueprint actors
    
    ## Blueprint Node Management
    - `add_blueprint_event_node(blueprint_name, event_type)` - Add event nodes
    - `add_blueprint_input_action_node(blueprint_name, action_name)` - Add input nodes
    - `add_blueprint_function_node(blueprint_name, function_name)` - Add function nodes
    - `add_blueprint_variable_get_node(blueprint_name, variable_name)` - Add variable getter nodes
    - `add_blueprint_variable_set_node(blueprint_name, variable_name)` - Add variable setter nodes
    - `add_blueprint_branch_node(blueprint_name)` - Add branch (if/else) nodes
    - `add_blueprint_sequence_node(blueprint_name)` - Add sequence nodes
    - `add_blueprint_delay_node(blueprint_name, delay_time)` - Add delay nodes
    - `add_blueprint_print_string_node(blueprint_name, message)` - Add print string nodes
    - `add_blueprint_math_node(blueprint_name, operation)` - Add math operation nodes
    - `connect_blueprint_nodes(blueprint_name, source_node_id, source_pin, target_node_id, target_pin)` - Connect nodes together
    
    ## Asset Creation Tools
    ### Animation Assets
    - `create_animation_blueprint(asset_name, skeleton_path, parent_class, save_path)` - Create an Animation Blueprint
    - `create_animation_composite(asset_name, animation_sequences, save_path)` - Create an Animation Composite
    - `create_animation_montage(asset_name, skeleton_path, animation_sequence, save_path)` - Create an Animation Montage
    - `create_aim_offset(asset_name, skeleton_path, save_path)` - Create an Aim Offset
    - `create_blend_space(asset_name, skeleton_path, axis_1_name, axis_1_min, axis_1_max, axis_2_name, axis_2_min, axis_2_max, save_path)` - Create a Blend Space
    - `create_pose_asset(asset_name, skeleton_path, save_path)` - Create a Pose Asset

    ### Blueprint Assets
    - `create_blueprint_class(asset_name, parent_class, save_path)` - Create a Blueprint Class

    ### Material Assets
    - `create_material(asset_name, save_path)` - Create a Material
    - `create_material_instance(asset_name, parent_material, save_path)` - Create a Material Instance

    ### Physics Assets
    - `create_physics_asset(asset_name, skeleton_path, save_path)` - Create a Physics Asset

    ### Artificial Intelligence
    - `create_behavior_tree(asset_name, save_path)` - Create a Behavior Tree
    - `create_blackboard(asset_name, save_path)` - Create a Blackboard

    ### Audio Assets
    - `create_sound_cue(asset_name, sound_wave_path, save_path)` - Create a Sound Cue

    ### Cinematics Assets
    - `create_level_sequence(asset_name, save_path)` - Create a Level Sequence

    ### User Interface
    - `create_widget_blueprint(asset_name, parent_class, save_path)` - Create a Widget Blueprint

    ### Niagara Effects
    - `create_niagara_system(asset_name, save_path)` - Create a Niagara System
    - `create_niagara_emitter(asset_name, save_path)` - Create a Niagara Emitter

    ### Level Assets
    - `create_level(asset_name, template_level, save_path)` - Create a Level

    ### Texture Assets
    - `create_render_target(asset_name, width, height, save_path)` - Create a Render Target

    ### Data Assets
    - `create_data_asset(asset_name, parent_class, save_path)` - Create a Data Asset

    ### Gameplay Assets
    - `create_game_mode(asset_name, save_path)` - Create a Game Mode Blueprint
    - `create_game_state(asset_name, save_path)` - Create a Game State Blueprint
    - `create_player_controller(asset_name, save_path)` - Create a Player Controller Blueprint
    
    ## Enhanced Node Tools
    - `create_rotating_actor(actor_type, blueprint_name, location, rotation, scale, rotation_speed, rotation_axis)` - Create an actor that rotates continuously
    - `add_blueprint_complete_rotation_logic(blueprint_name, rotation_speed, rotation_axis)` - Add complete rotation logic to an existing Blueprint
    - `create_precise_actor_at_location(actor_type, location, rotation, scale, actor_name, blueprint_name, use_blueprint)` - Create an actor at a precise location"""