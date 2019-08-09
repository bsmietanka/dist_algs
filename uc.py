import asyncio as aio
from collections import namedtuple

from utils import *
from beb import BestEffortBroadcast
from node_config import current_node, nodes
from pfd import failure_detector

Proposal = namedtuple('Proposal', ['round', 'proposals'])

class UniformConsensus():

    def __init__(self, upper_layer):
        self.upper_layer = upper_layer
        self.beb = BestEffortBroadcast(self)
        self.proposals = set()
        self.messages = {}

    async def propose(self, val):
        self.proposals.add(val)
        for r in range(len(nodes())):
            uc_m = Message(MessageType.UC, current_node(), Proposal(r, self.proposals))
            await self.beb.broadcast(uc_m)
            while True:
                working: set = await failure_detector()
                received_from = set([m.sender for m in self.messages.get(r, [])])
                proposals = [m.body.proposals for m in self.messages.get(r, [])]
                if working.issubset(received_from):
                    self.messages.pop(r)
                    self.proposals = set.union(*proposals)
                    break
        decision = min(self.proposals)
        self.proposals.clear()
        self.messages.clear()
        return decision

    async def deliver(self, message: Message):
        if message.type != MessageType.UC:
            raise ValueError('Uniform Consensus handles only messages with type UC')
        proposal = message.body
        if proposal.round not in self.messages:
            self.messages[proposal.round] = []
        self.messages[proposal.round].append(message)

    async def run(self):
        return await self.beb.run()

