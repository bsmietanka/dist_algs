import asyncio as aio
from utils import *
from node_config import nodes, timeout
from typing import Union

async def detect_failure(node: Node, timeout: float) -> Union[Node, None]:
    try:
        reader, writer = await aio.wait_for(aio.open_connection(node.addr, node.port), timeout)
    except aio.TimeoutError:
        return None
    writer.close()
    return node

async def failure_detector():
    calls = []
    for node in nodes():
        calls.append(detect_failure(node, timeout))
    working = await aio.gather(*calls)
    working = set(filter(None, working))
    return working
