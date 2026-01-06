"""Smart Assistant + Wallet Payments Module for OM1.

Bounty #367: OM1 + Smart Assistant + Wallet Payments
Implementation of smart home assistant integration with crypto wallet payments.
"""

from .assistant_connector import AssistantConnector
from .wallet_handler import WalletHandler
from .orchestrator import SmartAssistantWalletOrchestrator

__version__ = "1.0.0"
__all__ = [
    "AssistantConnector",
    "WalletHandler",
    "SmartAssistantWalletOrchestrator",
]
