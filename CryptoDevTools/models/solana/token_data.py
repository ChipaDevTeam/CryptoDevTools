from dataclasses import dataclass
from typing import List, Any

@dataclass
class HoldersData:
    """A structured class to hold token holder information."""
    total_holders: int
    top_holders: List[Any]

@dataclass
class TokenMetadata:
    """
    A structured class to hold token metadata information.
    """
    last_indexed_slot: int
    interface: str
    id: str
    content: dict
    authorities: dict[str, Any]
    compression: list[Any]
    collection: dict[str, Any]
    royalty: dict[str, Any]
    creators: list[dict[str, Any]]
    ownership: dict[str, Any]
    supply: dict[str, Any]
    mutable: bool
    burnt: bool
    token_info: dict[str, Any]