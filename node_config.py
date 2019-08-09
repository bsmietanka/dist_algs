from utils import *
import json
from typing import Sequence, TypeVar, Callable, Union

T = TypeVar('T')

__nodes: Sequence[Node] = []
__curr = None

timeout = 0.2

def read_configuration(config_path: str):
    with open(config_path, 'r') as f:
        config = json.load(f)
        return [Node(**item) for item in config['nodes']]

def find(f: Callable[[T], bool], seq: Sequence[T]) -> Union[T, None]:
    for item in seq:
        if f(item): 
            return item
    return None

def configure_node(config_path: str, node_name: str):
    global __nodes, __curr
    __nodes = read_configuration(config_path)
    __curr = find(lambda item: item.name == node_name, __nodes)
    if __curr == None:
        raise ValueError('Current node name not in the configuration file')

def nodes():
    # log/error if not configured?
    return __nodes

def current_node():
    return __curr
