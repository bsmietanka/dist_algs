import asyncio as aio
from utils import *
from node_config import current_node, nodes
from beb import BestEffortBroadcast
from pfd import failure_detector

_interval = 0.05

class UniformReliableBroadcast():
    def __init__(self, upper_layer):
        self.beb = BestEffortBroadcast(self)
        self.upper_layer = upper_layer
        self.pending = set()
        self.ack = dict()
        self.delivered = list()

    async def broadcast(self, message: Message):
        urb_m = Message(MessageType.URB, current_node(), message)
        self.pending.add(urb_m.body)
        await self.beb.broadcast(urb_m)

    async def deliver(self, message: Message):
        if message.type != MessageType.URB:
            raise ValueError('Uniform Reliable Broadcast handles only messages with type URB')

        if message.body not in self.ack:
            self.ack[message.body] = set()
        self.ack[message.body].add(message.sender)

        if message.body not in self.pending and message.body not in self.delivered:
            self.pending.add(message.body)
            message.sender = current_node()
            await self.beb.broadcast(message)

    def _can_deliver(self, message: Message, working: set):
        if working.issubset(self.ack.get(message, set())):
            return True
        return False

    async def _deliver(self):
        while True:
            working = await failure_detector()
            to_remove = []
            for m in self.pending:
                if self._can_deliver(m, working) and m not in self.delivered:
                    self.delivered.append(m)
                    to_remove.append(m)
                    await self.upper_layer.deliver(m)
            for m in to_remove:
                self.pending.remove(m)
            await aio.sleep(_interval)

    async def run(self):
        return await aio.gather(self.beb.run(), self._deliver())
