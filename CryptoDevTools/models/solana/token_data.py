from dataclasses import dataclass
from typing import List, Any

@dataclass
class HoldersData:
    """A structured class to hold token holder information."""
    total_holders: int
    top_holders: List[Any]