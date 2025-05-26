"""
AI Service module for Unreal MCP.

This module provides integration with AI services like OpenAI, Google Gemini,
and local LLM agents for generating Blueprint functions from natural language descriptions.
"""

import logging
import json
import requests
import os
from typing import Dict, Any, Optional, List

# Get logger
logger = logging.getLogger("UnrealMCP")

class AIServiceConfig:
    """Configuration for AI services."""
    
    def __init__(self):
        """Initialize with default configuration."""
        self.openai_api_key = ""
        self.gemini_api_key = ""
        self.local_agent_url = "http://localhost:8000"  # Default local agent URL
        self.selected_service = "local_agent"  # Default to local agent
        self.temperature = 0.7
        self.max_tokens = 2048
        
    def load_from_file(self, file_path: str) -> bool:
        """Load configuration from a JSON file."""
        try:
            with open(file_path, 'r') as f:
                config = json.load(f)
                
            if 'openai_api_key' in config:
                self.openai_api_key = config['openai_api_key']
            if 'gemini_api_key' in config:
                self.gemini_api_key = config['gemini_api_key']
            if 'local_agent_url' in config:
                self.local_agent_url = config['local_agent_url']
            if 'selected_service' in config:
                self.selected_service = config['selected_service']
            if 'temperature' in config:
                self.temperature = config['temperature']
            if 'max_tokens' in config:
                self.max_tokens = config['max_tokens']
                
            return True
        except Exception as e:
            logger.error(f"Error loading AI service config: {e}")
            return False
            
    def save_to_file(self, file_path: str) -> bool:
        """Save configuration to a JSON file."""
        try:
            config = {
                'openai_api_key': self.openai_api_key,
                'gemini_api_key': self.gemini_api_key,
                'local_agent_url': self.local_agent_url,
                'selected_service': self.selected_service,
                'temperature': self.temperature,
                'max_tokens': self.max_tokens
            }
            
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            with open(file_path, 'w') as f:
                json.dump(config, f, indent=4)
                
            return True
        except Exception as e:
            logger.error(f"Error saving AI service config: {e}")
            return False

class AIService:
    """Service for generating Blueprint code using AI."""
    
    def __init__(self, config: AIServiceConfig):
        """Initialize with the provided configuration."""
        self.config = config
        
    def generate_blueprint_function(self, 
                                   function_description: str,
                                   blueprint_context: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
        """
        Generate a Blueprint function from a natural language description.
        
        Args:
            function_description: Natural language description of the function
            blueprint_context: Optional context about the Blueprint (existing functions, variables, etc.)
            
        Returns:
            Dict containing the generated function details, or None if generation failed
        """
        if self.config.selected_service == "openai":
            return self._generate_with_openai(function_description, blueprint_context)
        elif self.config.selected_service == "gemini":
            return self._generate_with_gemini(function_description, blueprint_context)
        elif self.config.selected_service == "local":
            return self._generate_with_local_agent(function_description, blueprint_context)
        else:
            logger.error(f"Unsupported AI service: {self.config.selected_service}")
            return None
            
    def _generate_with_openai(self, 
                             function_description: str,
                             blueprint_context: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
        """Generate Blueprint function using OpenAI API."""
        try:
            if not self.config.openai_api_key:
                logger.error("OpenAI API key not configured")
                return None
                
            # Prepare the prompt
            prompt = self._prepare_prompt(function_description, blueprint_context)
            
            # Call OpenAI API
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.config.openai_api_key}"
            }
            
            payload = {
                "model": "gpt-4",  # Use GPT-4 for best results
                "messages": [
                    {"role": "system", "content": "You are an expert Unreal Engine Blueprint developer. Generate Blueprint function code based on the description."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": self.config.temperature,
                "max_tokens": self.config.max_tokens
            }
            
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=payload
            )
            
            if response.status_code != 200:
                logger.error(f"OpenAI API error: {response.status_code} - {response.text}")
                return None
                
            result = response.json()
            function_code = result['choices'][0]['message']['content']
            
            # Parse the generated code
            return self._parse_generated_code(function_code)
            
        except Exception as e:
            logger.error(f"Error generating with OpenAI: {e}")
            return None
            
    def _generate_with_gemini(self, 
                             function_description: str,
                             blueprint_context: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
        """Generate Blueprint function using Google Gemini API."""
        try:
            if not self.config.gemini_api_key:
                logger.error("Gemini API key not configured")
                return None
                
            # Prepare the prompt
            prompt = self._prepare_prompt(function_description, blueprint_context)
            
            # Call Gemini API
            headers = {
                "Content-Type": "application/json"
            }
            
            payload = {
                "contents": [
                    {
                        "parts": [
                            {"text": "You are an expert Unreal Engine Blueprint developer. Generate Blueprint function code based on the description."},
                            {"text": prompt}
                        ]
                    }
                ],
                "generationConfig": {
                    "temperature": self.config.temperature,
                    "maxOutputTokens": self.config.max_tokens
                }
            }
            
            response = requests.post(
                f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={self.config.gemini_api_key}",
                headers=headers,
                json=payload
            )
            
            if response.status_code != 200:
                logger.error(f"Gemini API error: {response.status_code} - {response.text}")
                return None
                
            result = response.json()
            function_code = result['candidates'][0]['content']['parts'][0]['text']
            
            # Parse the generated code
            return self._parse_generated_code(function_code)
            
        except Exception as e:
            logger.error(f"Error generating with Gemini: {e}")
            return None
            
    def _generate_with_local_agent(self, 
                                  function_description: str,
                                  blueprint_context: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
        """Generate Blueprint function using a local LLM agent."""
        try:
            if not self.config.local_agent_url:
                logger.error("Local agent URL not configured")
                return None
                
            # Prepare the prompt
            prompt = self._prepare_prompt(function_description, blueprint_context)
            
            # Call local agent API
            headers = {
                "Content-Type": "application/json"
            }
            
            payload = {
                "prompt": "You are an expert Unreal Engine Blueprint developer. Generate Blueprint function code based on the description.\n\n" + prompt,
                "temperature": self.config.temperature,
                "max_tokens": self.config.max_tokens
            }
            
            response = requests.post(
                f"{self.config.local_agent_url}/generate",
                headers=headers,
                json=payload
            )
            
            if response.status_code != 200:
                logger.error(f"Local agent API error: {response.status_code} - {response.text}")
                return None
                
            result = response.json()
            function_code = result['generated_text']
            
            # Parse the generated code
            return self._parse_generated_code(function_code)
            
        except Exception as e:
            logger.error(f"Error generating with local agent: {e}")
            return None
            
    def _prepare_prompt(self, 
                       function_description: str,
                       blueprint_context: Dict[str, Any] = None) -> str:
        """Prepare a prompt for the AI service."""
        prompt = f"Create an Unreal Engine Blueprint function that does the following:\n\n{function_description}\n\n"
        
        if blueprint_context:
            prompt += "Here is the context of the Blueprint:\n\n"
            
            if 'variables' in blueprint_context:
                prompt += "Existing variables:\n"
                for var in blueprint_context['variables']:
                    prompt += f"- {var['name']} ({var['type']})\n"
                prompt += "\n"
                
            if 'functions' in blueprint_context:
                prompt += "Existing functions:\n"
                for func in blueprint_context['functions']:
                    prompt += f"- {func['name']} ({', '.join(func['parameters'])})\n"
                prompt += "\n"
                
            if 'components' in blueprint_context:
                prompt += "Blueprint components:\n"
                for comp in blueprint_context['components']:
                    prompt += f"- {comp['name']} ({comp['type']})\n"
                prompt += "\n"
        
        prompt += """
Please provide your response in the following JSON format:

```json
{
  "function_name": "YourFunctionName",
  "description": "Brief description of what the function does",
  "return_type": "ReturnType",
  "parameters": [
    {"name": "param1", "type": "Type1", "description": "Description of param1"},
    {"name": "param2", "type": "Type2", "description": "Description of param2"}
  ],
  "local_variables": [
    {"name": "localVar1", "type": "Type1", "description": "Description of localVar1"}
  ],
  "nodes": [
    {
      "type": "FunctionEntry",
      "id": "node1",
      "position": [0, 0]
    },
    {
      "type": "FunctionCall",
      "id": "node2",
      "function": "PrintString",
      "target": "self",
      "parameters": {"InString": "Hello World"},
      "position": [200, 0]
    }
  ],
  "connections": [
    {"from_node": "node1", "from_pin": "Then", "to_node": "node2", "to_pin": "execute"}
  ],
  "required_structs": [
    {
      "name": "MyCustomStruct",
      "properties": [
        {"name": "Property1", "type": "Float"},
        {"name": "Property2", "type": "String"}
      ]
    }
  ],
  "required_enums": [
    {
      "name": "MyCustomEnum",
      "values": ["Value1", "Value2", "Value3"]
    }
  ]
}
```

Focus on creating a practical, efficient implementation that follows Unreal Engine best practices.
"""
        
        return prompt
        
    def _parse_generated_code(self, function_code: str) -> Dict[str, Any]:
        """Parse the generated code from the AI service."""
        try:
            # Extract JSON from the response (it might be wrapped in markdown code blocks)
            json_start = function_code.find('```json')
            if json_start != -1:
                json_start = function_code.find('{', json_start)
            else:
                json_start = function_code.find('{')
                
            json_end = function_code.rfind('}')
            
            if json_start == -1 or json_end == -1:
                logger.error("Could not find JSON in generated code")
                return None
                
            json_str = function_code[json_start:json_end+1]
            
            # Parse the JSON
            function_data = json.loads(json_str)
            
            # Validate the required fields
            required_fields = ['function_name', 'nodes', 'connections']
            for field in required_fields:
                if field not in function_data:
                    logger.error(f"Generated function data missing required field: {field}")
                    return None
                    
            return function_data
            
        except Exception as e:
            logger.error(f"Error parsing generated code: {e}")
            return None

# Create config directory if it doesn't exist
config_dir = os.path.expanduser("~/.unreal_mcp")
if not os.path.exists(config_dir):
    os.makedirs(config_dir)

# Config file path
config_file = os.path.join(config_dir, "ai_config.json")

# Initialize configuration
config = AIServiceConfig()
if os.path.exists(config_file):
    config.load_from_file(config_file)
else:
    # Create default config
    config.save_to_file(config_file)

# Create AI service
ai_service = AIService(config)
