import json

from typing import Tuple, List

from lab6.data import Node


class FlyweightFactory:
    def __init__(self, data=None):
        self._tree_root = data if data else Node('Root')

    @property
    def data(self) -> Node:
        return self._tree_root

    def add(self, name: str, coords: Tuple[int, int]):
        last_node = self._get_last_node(name)
        last_node.coords = coords

    def get(self, name: str) -> Tuple[int, int]:
        last_node = self._get_last_node(name)
        return last_node.coords

    def _get_last_node(self, name: str) -> Node:
        node = Node.from_str(name)
        tree_node = self._tree_root

        while node.next_nodes:
            if (i := self._index_of(tree_node.next_nodes, node)) == -1:
                tree_node.next_nodes.append(Node(node.value))

            tree_node = tree_node.next_nodes[i]
            node = node.next_nodes[0]

        if (i := self._index_of(tree_node.next_nodes, node)) == -1:
            tree_node.next_nodes.append(Node(node.value))

        return tree_node.next_nodes[i]

    @staticmethod
    def _index_of(nodes: List[Node], node_to_find: Node) -> int:
        for i, node in enumerate(nodes):
            if node.value == node_to_find.value:
                return i
        return -1

    def to_json(self):
        return json.dumps(self._tree_root, cls=AllFieldsEncoder)

    @classmethod
    def _from_json(cls, json_string: str):
        json_ = json.loads(json_string)
        return cls(data=Node.from_json(json_))

    @classmethod
    def from_file(cls, filename: str):
        with open(filename, 'r') as file:
            data = ''.join(file.readlines())
            return cls._from_json(data)

    def save(self, filename: str):
        with open(filename, 'w') as file:
            file.write(self.to_json())


class AllFieldsEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__