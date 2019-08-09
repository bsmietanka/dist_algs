from enum import IntEnum, auto
from typing import Any
from datetime import datetime

class MessageType(IntEnum):
    ACK = auto()
    ONAR = auto()
    UC = auto()
    BEB = auto()
    URB = auto()
    APP = auto()

class Node():
    def __init__(self, name: str, addr: str, port: int):
        self.name = name
        self.addr = addr
        self.port = port
    
    def __repr__(self):
        return f'Node: {self.name}/{self.addr}:{self.port}'

    def __eq__(self, other):
        if not isinstance(other, Node):
            return False
        return self.name == other.name and self.addr == other.addr and self.port == other.port

    def __hash__(self):
        return hash((self.name, self.addr, self.port))

class Message():
    def __init__(self, t: MessageType, sender: Node, body: Any):
        self.type = t
        self.sender = sender
        self.body = body
        self.t = datetime.now()

    def __repr__(self):
        return f'[{self.type}] [{self.sender}] : {self.body}'

    def __eq__(self, other):
        if not isinstance(other, Message):
            return False
        return self.type == other.type and self.sender == other.sender and self.body == other.body and self.t == other.t

    def __hash__(self):
        return hash((self.type, self.sender, self.body, self.t))
