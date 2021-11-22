from __future__ import annotations
from typing import Iterator, List, TYPE_CHECKING

from lab5.events import Event
from lab5.fire_engines import FireEngine, ReadyState

if TYPE_CHECKING:
    from lab5.departments import Department


class ClosestEnginesIterator(Iterator):
    def __init__(self, departments: List['Department'], event: Event):
        self._departments = sorted(departments, key=lambda d: self.distance(d.coords, event.coords))
        self._department_i = 0
        self._engine_i = 0

    @staticmethod
    def distance(coord_1, coord_2):
        x1, y1 = coord_1
        x2, y2 = coord_2
        return abs((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1))

    def __iter__(self) -> ClosestEnginesIterator:
        self._department_i = 0
        self._engine_i = 0
        return self

    def __next__(self) -> FireEngine:
        ready_engine = None

        while not ready_engine:
            if self._department_i < len(self._departments):
                department = self._departments[self._department_i]

                if self._engine_i < len(department.engines):
                    engine = department.engines[self._engine_i]
                    self._engine_i += 1
                    if engine.state == ReadyState():
                        ready_engine = engine
                        break
                else:
                    self._engine_i = 0
                    self._department_i += 1
                    continue

            else:
                raise StopIteration

        return ready_engine