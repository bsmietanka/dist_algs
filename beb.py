import asyncio as aio
from utils import *
from pl import PerfectLink
from node_config import current_node, nodes, timeout

class BestEffortBroadcast():
    def __init__(self, upper_layer):
        self.pl = PerfectLink(self)
        self.upper_layer = upper_layer

    async def broadcast(self, message: Message):
        beb_m = Message(MessageType.BEB, current_node(), message)
        calls = []
        for node in nodes():
            calls.append(self.pl.send(beb_m, node, timeout))
        await aio.gather(*calls)

    async def deliver(self, message: Message):
        if message.type == MessageType.ACK:
            return await self.upper_layer.deliver(message) # if message is of type ACK let upper_layer handle it
        elif message.type != MessageType.BEB:
            raise ValueError('Best Effort Broadcast handles only messages with type ACK or BEB')
        await self.upper_layer.deliver(message.body)

    async def run(self):
        return await self.pl.run()
