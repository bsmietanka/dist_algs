import asyncio as aio
import json
from utils import *
from typing import Callable, TypeVar
from node_config import current_node

Layer = TypeVar('Layer')

class ConsoleNode():
    def __init__(self, class_name):
        self.lower_layer = class_name(self)

    async def deliver(self, message: Message):
        if message.type != MessageType.APP:
            raise ValueError()
        print(f'Message body: {message.body}')

    async def broadcast(self, message):
        m = Message(MessageType.APP, current_node(), message)
        await self.lower_layer.broadcast(m)

    async def read(self):
        return await self.lower_layer.read()

    async def write(self, val):
        await self.lower_layer.write(val)

    async def propose(self, val):
        return await self.lower_layer.propose(val)

    async def run(self):
        return await self.lower_layer.run()
