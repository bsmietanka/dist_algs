import asyncio as aio
from collections import namedtuple
from datetime import datetime

from beb import BestEffortBroadcast
from node_config import current_node, nodes, timeout
from pfd import failure_detector
from pl import PerfectLink
from utils import *

_interval = 0.05

Register = namedtuple('Register', ['ts', 'val'])

class OneNAtomicRegister():

    def __init__(self, upper_layer):
        self.beb = BestEffortBroadcast(self)
        self.pl = self.beb.pl
        self.writeset = set()
        self.reg = Register(datetime.min, None)
        self.upper_layer = upper_layer

    async def read(self):
        message = Message(MessageType.ONAR, current_node(), self.reg)
        await self.beb.broadcast(message)
        await self.wait_all_ack()
        return self.reg.val

    async def write(self, val):
        message = Message(MessageType.ONAR, current_node(), Register(datetime.now(), val))
        await self.beb.broadcast(message)
        await self.wait_all_ack()

    async def deliver(self, message: Message):
        if message == None:
            print('something')
        if message.type == MessageType.ONAR:
            m_reg = message.body
            if m_reg.ts > self.reg.ts:
                self.reg = m_reg
            ack_m = Message(MessageType.ACK, current_node(), None)
            await self.pl.send(ack_m, message.sender, timeout)
        elif message.type == MessageType.ACK:
            self.writeset.add(message.sender)
        else:
            raise ValueError('One-N Atomic Register handles only messages with type ONAR or ACK')

    async def wait_all_ack(self):
        while True:
            working = await failure_detector()
            if working.issubset(self.writeset):
                self.writeset.clear()
                return
            await aio.sleep(_interval)

    async def run(self):
        return await self.beb.run()
