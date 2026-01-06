"""Smart Assistant Connector for OM1.

Handles integration with Home Assistant, Alexa, Siri, and other voice assistants.
"""

import asyncio
import json
import logging
from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Dict, Optional

import aiohttp

logger = logging.getLogger(__name__)


class AssistantType(Enum):
    """Supported assistant types."""
    HOME_ASSISTANT = "home_assistant"
    ALEXA = "alexa"
    SIRI = "siri"
    GOOGLE_ASSISTANT = "google_assistant"


class AssistantConnector(ABC):
    """Base class for assistant connectors."""

    def __init__(self, config: Dict[str, Any]):
        """Initialize the assistant connector.
        
        Args:
            config: Configuration dictionary with assistant details
        """
        self.config = config
        self.session: Optional[aiohttp.ClientSession] = None

    @abstractmethod
    async def connect(self) -> bool:
        """Connect to the assistant service.
        
        Returns:
            True if connection successful, False otherwise
        """
        pass

    @abstractmethod
    async def disconnect(self) -> None:
        """Disconnect from the assistant service."""
        pass

    @abstractmethod
    async def send_command(self, command: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Send a command to the assistant.
        
        Args:
            command: Command name (e.g., 'order', 'pay')
            params: Command parameters
            
        Returns:
            Command response
        """
        pass

    @abstractmethod
    async def receive_order(self) -> Optional[Dict[str, Any]]:
        """Receive order from voice command.
        
        Returns:
            Order details or None if no order received
        """
        pass


class HomeAssistantConnector(AssistantConnector):
    """Home Assistant connector implementation."""

    async def connect(self) -> bool:
        """Connect to Home Assistant via REST API."""
        try:
            self.session = aiohttp.ClientSession()
            url = f"{self.config['ha_url']}/api/"
            headers = {"Authorization": f"Bearer {self.config['ha_token']}"}
            
            async with self.session.get(url, headers=headers) as resp:
                if resp.status == 200:
                    logger.info("Connected to Home Assistant")
                    return True
            return False
        except Exception as e:
            logger.error(f"Failed to connect to Home Assistant: {e}")
            return False

    async def disconnect(self) -> None:
        """Disconnect from Home Assistant."""
        if self.session:
            await self.session.close()

    async def send_command(self, command: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Send command to Home Assistant."""
        if not self.session:
            return {"status": "error", "message": "Not connected"}

        url = f"{self.config['ha_url']}/api/services/{params.get('domain', 'script')}/{command}"
        headers = {"Authorization": f"Bearer {self.config['ha_token']}"}
        
        try:
            async with self.session.post(url, json=params, headers=headers) as resp:
                return await resp.json()
        except Exception as e:
            logger.error(f"Error sending command: {e}")
            return {"status": "error", "message": str(e)}

    async def receive_order(self) -> Optional[Dict[str, Any]]:
        """Receive order from Home Assistant input text sensor."""
        if not self.session:
            return None

        url = f"{self.config['ha_url']}/api/states/input_text.om1_order"
        headers = {"Authorization": f"Bearer {self.config['ha_token']}"}
        
        try:
            async with self.session.get(url, headers=headers) as resp:
                data = await resp.json()
                if data["state"] and data["state"] != "unknown":
                    return {"order_text": data["state"]}
            return None
        except Exception as e:
            logger.error(f"Error receiving order: {e}")
            return None


class AlexaConnector(AssistantConnector):
    """Amazon Alexa connector implementation."""

    async def connect(self) -> bool:
        """Connect to Alexa Skills service."""
        try:
            self.session = aiohttp.ClientSession()
            # Alexa connection would be handled through skill invocation
            logger.info("Alexa connector initialized")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize Alexa: {e}")
            return False

    async def disconnect(self) -> None:
        """Disconnect from Alexa."""
        if self.session:
            await self.session.close()

    async def send_command(self, command: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Send response back to Alexa user."""
        return {"status": "success", "speech": params.get("message", "")}

    async def receive_order(self) -> Optional[Dict[str, Any]]:
        """Receive order from Alexa voice command."""
        # In production, this would receive from Alexa Lambda function
        return None


def get_connector(assistant_type: AssistantType, config: Dict[str, Any]) -> AssistantConnector:
    """Factory function to get appropriate connector.
    
    Args:
        assistant_type: Type of assistant
        config: Configuration for the assistant
        
    Returns:
        Appropriate connector instance
    """
    if assistant_type == AssistantType.HOME_ASSISTANT:
        return HomeAssistantConnector(config)
    elif assistant_type == AssistantType.ALEXA:
        return AlexaConnector(config)
    else:
        raise ValueError(f"Unsupported assistant type: {assistant_type}")
