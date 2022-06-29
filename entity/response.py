from dataclasses import dataclass
from typing import Optional


@dataclass
class Response:
    id: Optional[int]
    time: Optional[float]
    name: str
