"""
HTTP Client module for Unreal MCP.

This module provides a simple HTTP client for making API requests.
"""

import logging
import requests
from typing import Dict, Any, Optional

# Get logger
logger = logging.getLogger("UnrealMCP")

class HTTPClient:
    """Simple HTTP client for making API requests."""
    
    @staticmethod
    def get(url: str, headers: Dict[str, str] = None, params: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
        """
        Make a GET request to the specified URL.
        
        Args:
            url: The URL to request
            headers: Optional headers to include
            params: Optional query parameters
            
        Returns:
            Dict containing the response JSON, or None if the request failed
        """
        try:
            response = requests.get(url, headers=headers, params=params)
            
            if response.status_code != 200:
                logger.error(f"HTTP GET error: {response.status_code} - {response.text}")
                return None
                
            return response.json()
            
        except Exception as e:
            logger.error(f"Error making HTTP GET request: {e}")
            return None
    
    @staticmethod
    def post(url: str, headers: Dict[str, str] = None, json: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
        """
        Make a POST request to the specified URL.
        
        Args:
            url: The URL to request
            headers: Optional headers to include
            json: Optional JSON body
            
        Returns:
            Dict containing the response JSON, or None if the request failed
        """
        try:
            response = requests.post(url, headers=headers, json=json)
            
            if response.status_code != 200:
                logger.error(f"HTTP POST error: {response.status_code} - {response.text}")
                return None
                
            return response.json()
            
        except Exception as e:
            logger.error(f"Error making HTTP POST request: {e}")
            return None
