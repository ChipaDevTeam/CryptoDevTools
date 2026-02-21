"""
WalletGenerator — generates Solana keypairs using solders.
The private key is returned as base58 so it can be encrypted and stored
server-side; the public address is safe to display to the user.
"""
import base64
import base58  # pip install base58
from solders.keypair import Keypair


class WalletGenerator:
    """Generate and manage Solana wallets."""

    @staticmethod
    def generate() -> dict:
        """
        Generate a new Solana keypair.

        Returns:
            {
                "address":     str  — base58 public key (wallet address)
                "private_key": str  — base58-encoded 64-byte secret key
                "private_key_bytes": bytes — raw 64-byte secret for encryption
            }
        """
        kp = Keypair()
        secret_bytes = bytes(kp)          # 64 bytes: 32-byte seed + 32-byte pubkey
        private_b58 = base58.b58encode(secret_bytes).decode()
        return {
            "address": str(kp.pubkey()),
            "private_key": private_b58,
            "private_key_bytes": secret_bytes,
        }

    @staticmethod
    def from_private_key(private_key_b58: str) -> "Keypair":
        """Reconstruct a Keypair from a base58-encoded private key."""
        raw = base58.b58decode(private_key_b58)
        return Keypair.from_bytes(raw)

    @staticmethod
    def address_from_private_key(private_key_b58: str) -> str:
        """Return just the public address from a stored private key."""
        kp = WalletGenerator.from_private_key(private_key_b58)
        return str(kp.pubkey())
