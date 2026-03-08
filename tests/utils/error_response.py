from dataclasses import dataclass
from typing import Optional


@dataclass
class ErrorResponse:
    """DTO representing a standard API error response."""
    name: Optional[str] = None
    message: Optional[str] = None
    error: Optional[str] = None
    status: Optional[int] = None
    path: Optional[str] = None
    timestamp: Optional[str] = None
