from typing import Tuple

from flyweight import FlyweightFactory
from lab6.data import Node


class MigrantRepository:
    def __init__(self, _flyweights=None):
        self._flyweights = _flyweights if _flyweights else FlyweightFactory()

    @property
    def data(self) -> Node:
        return self._flyweights.data

    def add(self, name: str, coords: Tuple[int, int]):
        name = ' '.join(name_part.capitalize() for name_part in name.split(' '))
        self._flyweights.add(name, coords)

    def get(self, name: str) -> Tuple[int, int]:
        name = ' '.join(name_part.capitalize() for name_part in name.split(' '))
        return self._flyweights.get(name)

    def to_json(self):
        return self._flyweights.to_json()

    @classmethod
    def from_file(cls, filename: str):
        return cls(FlyweightFactory.from_file(filename))

    def save(self, filename: str):
        self._flyweights.save(filename)