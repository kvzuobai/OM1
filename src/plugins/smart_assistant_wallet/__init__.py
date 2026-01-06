"""Smart Assistant + Wallet Payments Module for OM1.

Bounty #367: OM1 + Smart Assistant + Wallet Payments
Implementation of smart home assistant integration with crypto wallet payments.
"""

from .assistant_connector import AssistantConnector, get_connector, AssistantType
from .wallet_handler import WalletHandler, get_wallet_handler, PaymentNetwork, TransactionStatus, Transaction

__version__ = "1.0.0"
__all__ = [
    "AssistantConnector",
    "WalletHandler",
    "get_connector",
    "get_wallet_handler",
    "AssistantType",
    "PaymentNetwork",
    "TransactionStatus",
    "Transaction",
]
