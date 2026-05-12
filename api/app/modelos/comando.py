from dataclasses import dataclass


@dataclass
class CommandMapping:
    key: str
    kit: str
    device_type: str
    number: int
    topic: str
    coil_address: int
    description: str