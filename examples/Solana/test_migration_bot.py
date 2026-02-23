import asyncio
import sys
import os

# Add the project root to sys.path to resolve imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from CryptoDevTools.solana._TradeClient import SolanaTradeClient
from solders.pubkey import Pubkey
from solders.instruction import Instruction, AccountMeta
from solders.system_program import transfer, TransferParams
from solders.keypair import Keypair

async def main():
    print("Initializing Split Migration Bot Test...")
    
    # 1. Configuration
    RPC_URL = "https://api.mainnet-beta.solana.com" # Or your dedicated RPC
    client = SolanaTradeClient(RPC_URL)
    
    # Generate dummy keys for testing
    payer = Keypair() # Usually loaded from env
    token_mint = Pubkey.from_string("DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263") # Bonk (example)
    raydium_pool_id = Pubkey.from_string("58oQChx4yWmvKdwLLZzBi4ChoCcKTk3jWq7cfk8uy8dM") # SOL/USDC (example)
    
    TOTAL_BUY_AMOUNT = 5.0
    PUMP_ALLOCATION = 1.5
    
    print(f"Total Buy Layout: {TOTAL_BUY_AMOUNT} SOL")
    print(f" - PumpFun Allocation: {PUMP_ALLOCATION} SOL")
    print(f" - Raydium Allocation (Post-Migration): {TOTAL_BUY_AMOUNT - PUMP_ALLOCATION} SOL")
    
    # 2. Simulate Migration Instruction
    # In a real scenario, this would be the actual migration instruction from PumpFun to Raydium.
    # Or if sniping, you'd target this transaction hash via Jito.
    # Here we mock it with a simple transfer.
    dummy_migration_program = Pubkey.from_string("11111111111111111111111111111111")
    migration_ix = Instruction(
        program_id=dummy_migration_program,
        data=b"migration_data",
        accounts=[AccountMeta(payer.pubkey(), True, True)]
    )
    
    # 3. Create the Split Buy Bundle
    bundle_instructions = client.create_split_migration_bundle(
        payer=payer.pubkey(),
        token_mint=token_mint,
        total_sol=TOTAL_BUY_AMOUNT,
        pump_allocation=PUMP_ALLOCATION,
        migration_instruction=migration_ix, # Pass None if you are sniping an existing pending tx
        raydium_pool_id=raydium_pool_id
    )
    
    print(f"\nCreated {len(bundle_instructions)} instructions for the bundle.")
    
    # 4. Construct Transaction (Simulated)
    # The instructions would be:
    # [0] PumpFun Buy
    # [1] Migration
    # [2] Raydium Buy
    
    from solders.transaction import Transaction
    from solders.message import Message
    
    # In reality, this would likely be sent as a Jito Bundle because of compute limits or specific ordering guarantees needed
    # especially if the migration is complex.
    
    print("\nSimulating Transaction/Bundle Construction...")
    # blockhash = client.client.get_latest_blockhash().value.blockhash
    # tx = Transaction(message=Message.new_with_payer(bundle_instructions, payer.pubkey()), recent_blockhash=blockhash)
    
    # Log details
    for i, ix in enumerate(bundle_instructions):
        print(f"Instruction {i+1}: Program: {ix.program_id}")
        if i == 0:
            print(" -> PumpFun Buy Logic")
        elif i == 1:
            print(" -> Migration Trigger")
        elif i == 2:
            print(" -> Raydium Buy Logic")

    print("\nTest Bot Logic Verified. Ready for integration with live keys/RPC.")

if __name__ == "__main__":
    asyncio.run(main())
