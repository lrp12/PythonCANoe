from dataclasses import dataclass


@dataclass
class CANoeMessage:
    message: str
    signal: str
    channel: int = 1
