from __future__ import annotations

import json

from typing import List, Dict


class Node:
    def __init__(self, value, coords=None, next_nodes=None):
        self.value = value
        self.coords = coords
        self.next_nodes: List[Node] = next_nodes if next_nodes else []

    @classmethod
    def from_json(cls, json_: Dict) -> Node:
        value = json_['value']
        coords = json_['coords']
        coords_tuple = tuple(coords) if coords else None
        next_nodes = [cls.from_json(node) for node in json_['next_nodes']]
        return cls(value=value,
                   coords=coords_tuple,
                   next_nodes=next_nodes)

    @classmethod
    def from_json_str(cls, json_string: str):
        json_ = json.loads(json_string)
        return cls.from_json(json_)

    @classmethod
    def from_values(cls, values: List[str]):
        base_node = node = cls(values[0])

        for value in values[1:]:
            next_node = Node(value)
            node.next_nodes.append(next_node)
            node = node.next_nodes[0]

        return base_node

    @classmethod
    def from_str(cls, string: str):
        return cls.from_values(string.split(' '))

    def yield_values(self):
        node = self
        while node.next_nodes:
            yield node.value
            node = node.next_nodes[0]
        yield str(node.value)

    def __str__(self):
        return ' -> '.join(self.yield_values())

    def __repr__(self):
        return f"Node('{self.value}')"