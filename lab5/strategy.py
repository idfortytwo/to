import random
import time
from abc import ABC, abstractmethod
from threading import Thread
from typing import List, Callable, TYPE_CHECKING

from lab5.iterators import ClosestEnginesIterator
from lab5.events import Event
from lab5.fire_engines import FireEngine, FireEngineSquad, BusyState, ReadyState

if TYPE_CHECKING:
    from lab5.departments import Department


class PreparationStrategy(ABC):
    def __init__(self, departments: List['Department']):
        self._departments = departments
        self._squad: FireEngineSquad

    @abstractmethod
    def request_squad(self, event: Event) -> FireEngineSquad:
        pass

    def _request_n_engines(self, event: Event, n: int) -> List[FireEngine]:
        engines = []
        engines_it = iter(ClosestEnginesIterator(self._departments, event))
        accepted_engines = 0

        while accepted_engines < n:
            engine = next(engines_it)
            engines.append(engine)
            accepted_engines += 1

        return engines

    def __str__(self):
        return f'{self.__class__.__name__}'


class FirePreparationStrategy(PreparationStrategy):
    def request_squad(self, event: Event):
        engines = self._request_n_engines(event, 3)
        squad = FireEngineSquad(engines, NormalExecutionStrategy)
        return squad


class LocalThreatPreparationStrategy(PreparationStrategy):
    def request_squad(self, event: Event):
        engines = self._request_n_engines(event, 2)
        squad = FireEngineSquad(engines, NormalExecutionStrategy)
        return squad


class FAFirePreparationStrategy(PreparationStrategy):
    def request_squad(self, event: Event):
        engines = self._request_n_engines(event, 3)
        squad = FireEngineSquad(engines, FalseAlarmExecutionStrategy)
        return squad


class FALocalThreatPreparationStrategy(PreparationStrategy):
    def request_squad(self, event: Event):
        engines = self._request_n_engines(event, 2)
        squad = FireEngineSquad(engines, FalseAlarmExecutionStrategy)
        return squad


class ExecutionStrategy(ABC):
    def __init__(self, squad: FireEngineSquad):
        self._squad = squad

    @staticmethod
    def _next_step(delay: float, func: Callable):
        thread = Thread(target=lambda: (time.sleep(delay), func()))
        thread.start()

    @abstractmethod
    def send(self):
        pass


class NormalExecutionStrategy(ExecutionStrategy):
    def _depart(self):
        print('D -> [X] ' + ', '.join(str(engine) for engine in self._squad))
        for engine in self._squad:
            engine.set_state(BusyState())

        travel_delay = random.random() * 3
        self._next_step(travel_delay, self._do_work)

    def _do_work(self):
        print('     […] ' + ', '.join(str(engine) for engine in self._squad))

        # work_delay = 5 + random.random() * 20
        work_delay = 5 + random.random() * 1
        self._next_step(work_delay, self._depart_back)

    def _depart_back(self):
        print('  <- [ ] ' + ', '.join(str(engine) for engine in self._squad))

        travel_delay = random.random() * 3
        self._next_step(travel_delay, self._return)

    def _return(self):
        print('D <- [ ] ' + ', '.join(str(engine) for engine in self._squad))
        for engine in self._squad:
            engine.set_state(ReadyState())

    def send(self):
        self._depart()


class FalseAlarmExecutionStrategy(ExecutionStrategy):
    def _depart(self):
        print('D ->  _  ' + ', '.join(str(engine) for engine in self._squad))
        for engine in self._squad:
            engine.set_state(BusyState())

        travel_delay = random.random() * 3
        self._next_step(travel_delay, self._return)

    def _return(self):
        print('D <-  _  ' + ', '.join(str(engine) for engine in self._squad))
        for engine in self._squad:
            engine.set_state(ReadyState())

    def send(self):
        self._depart()