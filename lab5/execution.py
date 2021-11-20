from abc import ABC, abstractmethod
from typing import List

from lab5.iterators import ClosestEnginesIterator
from lab5.events import Event
from lab5.fire_engines import FireEngine


class Strategy(ABC):
    def __init__(self, departments: List):
        self.departments = departments

    @abstractmethod
    def request_engines(self, event: Event) -> List[FireEngine]:
        pass

    def _request_n_engines(self, event: Event, n: int) -> List[FireEngine]:
        engines = []
        engines_it = iter(ClosestEnginesIterator(self.departments, event))
        accepted_engines = 0

        while accepted_engines < n:
            engine = next(engines_it)
            engines.append(engine)
            accepted_engines += 1

        return engines


class FireStrategy(Strategy):
    def request_engines(self, event: Event):
        return self._request_n_engines(event, 3)


class LocalThreatStrategy(Strategy):
    def request_engines(self, event: Event):
        return self._request_n_engines(event, 2)