import argparse
import asyncio as aio
import sys

from aioconsole import ainput

from console_node import ConsoleNode
from beb import BestEffortBroadcast
from urb import UniformReliableBroadcast
from onar import OneNAtomicRegister
from uc import UniformConsensus
from node_config import configure_node, current_node, nodes
from utils import *

node = None

async def handle_input():
    while True:
        line = await ainput("[b]roadcast [r]ead [w]rite [p]ropose [e]xit\n")
        if line == 'b':
            line = await ainput("Message: ")
            if not line:
                line = 'Hello World!'
            await node.broadcast(line)
        elif line == 'e':
            sys.exit(1)
        elif line == 'r':
            print(f'Value read: {await node.read()}')
        elif line == 'w':
            line = await ainput("Write value: ")
            if not line:
                line = 'Hello World!'
            await node.write(line)
        elif line == 'p':
            line = await ainput("Propose value: ")
            if not line:
                line = 'Hello World!'
            print(f'Final proposal: {await node.propose(line)}')
        else:
            print("Incorrect input")

async def main(args):
    configure_node(args.config_path, args.node_name)
    global node
    node = ConsoleNode(UniformConsensus)
    await aio.gather(node.run(), handle_input())

parser = argparse.ArgumentParser(description='Run distributed algorithm nodes')
parser.add_argument('config_path', metavar='path', type=str, help='Path to config .json')
parser.add_argument('node_name', metavar='name', type=str, help='Current node name')
parser.add_argument('-b', action='store_true', help='This node will broadcast message')
args = parser.parse_args()

aio.run(main(args))
