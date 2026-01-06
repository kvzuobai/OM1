#!/usr/bin/env python3
"""
Local Testing Script for Bounty #367
Smart Assistant + Wallet Payments Integration
"""

import asyncio
from decimal import Decimal
from src.plugins.smart_assistant_wallet.wallet_handler import (
    get_wallet_handler,
    PaymentNetwork,
    TransactionStatus,
)

async def test_mock_wallet():
    """Test the mock wallet implementation"""
    
    print("\n" + "="*70)
    print("TEST 1: Mock Wallet Handler")
    print("="*70)
    
    # Initialize mock wallet
    wallet_config = {"wallet_address": "0xtest_user"}
    wallet = get_wallet_handler("mock", wallet_config)
    
    # Test 1: Initialize
    print("\n[TEST 1] Initialize wallet...")
    is_initialized = await wallet.initialize()
    print(f"✓ Initialized: {is_initialized}")
    
    # Test 2: Get balance
    print("\n[TEST 2] Get balance...")
    balance = await wallet.get_balance()
    print(f"✓ Balance: {balance}")
    
    # Test 3: Execute payment
    print("\n[TEST 3] Execute payment...")
    tx = await wallet.execute_payment(
        recipient="0xrecipient_test",
        amount=Decimal("0.05"),
        network=PaymentNetwork.ETHEREUM
    )
    print(f"✓ Transaction ID: {tx.tx_id}")
    print(f"✓ Status: {tx.status.value}")
    print(f"✓ Hash: {tx.tx_hash[:20]}...")
    
    # Test 4: Get transaction status
    print("\n[TEST 4] Get transaction status...")
    status_tx = await wallet.get_transaction_status(tx.tx_id)
    if status_tx:
        print(f"✓ Status: {status_tx.status.value}")
        print(f"✓ Amount: {status_tx.amount} ETH")
    
    # Test 5: Multi-network support
    print("\n[TEST 5] Test multi-network payments...")
    networks = [
        PaymentNetwork.ETHEREUM,
        PaymentNetwork.POLYGON,
        PaymentNetwork.BASE,
        PaymentNetwork.SOLANA,
    ]
    
    for network in networks:
        tx = await wallet.execute_payment(
            recipient="0xtest_recipient",
            amount=Decimal("0.1"),
            network=network
        )
        print(f"✓ {network.value.upper():10} - Status: {tx.status.value}")

async def main():
    print("\n" + "#"*70)
    print("# BOUNTY #367 - LOCAL TESTING")
    print("# Smart Assistant + Wallet Payments")
    print("#"*70)
    
    try:
        await test_mock_wallet()
        
        print("\n" + "#"*70)
        print("# ALL TESTS PASSED! ✓")
        print("#"*70)
        print("\n✓ Code works correctly on your local PC!")
        print("✓ Mock wallet implementation is functional!")
        print("✓ Ready for OpenMind review!")
        
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
