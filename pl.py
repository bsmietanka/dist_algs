import asyncio as aio
import pickle
from utils import *
from node_config import current_node

class PerfectLink():
    def __init__(self, upper_layer):
        self.upper_layer = upper_layer

    async def handle_messages(self, reader, writer):
        data = await reader.read(1000)
        # handle echo messages
        if not data:
            return
        message = pickle.loads(data)
        await self.upper_layer.deliver(message)
        writer.close()

    async def send(self, message: Message, target: Node, timeout: float):
        try:
            _, writer = await aio.wait_for(aio.open_connection(target.addr, target.port), timeout)
        except aio.TimeoutError:
            return
        writer.write(pickle.dumps(message))
        writer.close()

    async def run(self):
        svr = await aio.start_server(self.handle_messages, current_node().addr, current_node().port)
        return svr.serve_forever()
