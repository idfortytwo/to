from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Type

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from lab5.strategy import ExecutionStrategy


class FireEngineState(ABC):
    @property
    def fire_engine(self) -> FireEngine:
        return self._fire_engine

    @fire_engine.setter
    def fire_engine(self, fire_engine: FireEngine) -> None:
        self._fire_engine = fire_engine

    @abstractmethod
    def handle_ready(self) -> None:
        pass

    @abstractmethod
    def handle_busy(self) -> None:
        pass

    def __eq__(self, other):
        if isinstance(other, FireEngineState):
            return self.__class__ == other.__class__
        return False

    def __hash__(self):
        return hash(self.__class__)


class ReadyState(FireEngineState):
    def handle_ready(self) -> None:
        pass

    def handle_busy(self) -> None:
        self.fire_engine.set_state(BusyState())

    def __str__(self):
        return 'Ready'


class BusyState(FireEngineState):
    def handle_ready(self) -> None:
        self.fire_engine.set_state(ReadyState())

    def handle_busy(self) -> None:
        pass

    def __str__(self):
        return 'Busy'


class FireEngine:
    def __init__(self, name: str, state: FireEngineState = ReadyState()):
        self._name = name
        self.set_state(state)

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    def set_state(self, state: FireEngineState):
        self._state = state
        self._state._fire_engine = self

    def request_ready(self):
        self._state.handle_ready()

    def request_busy(self):
        self._state.handle_busy()

    def __repr__(self):
        return f"FireEngine('{self.name}', {self._state})"


class FireEngineSquad:
    def __init__(self, engines: List[FireEngine], Strategy: Type[ExecutionStrategy]):
        self._engines = engines
        self._strategy = Strategy(self)

    @property
    def engines(self):
        return self._engines

    def __iter__(self):
        return iter(self._engines)

    def send(self):
        self._strategy.send()