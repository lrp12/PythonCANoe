from dataclasses import dataclass
from typing import Union, List


@dataclass
class CANoeMessage:
    message: str
    signal: str
    channel: int
