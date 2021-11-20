from typing import List
from collections.abc     import Iterator

from lab5.fire_engines import FireEngine


class Department:
    def __init__(self, title: str):
        self.title = title
        self.engines: List[FireEngine] = [FireEngine(f'{self.title}-{i}') for i in range(5)]

    def print_state(self):
        for engine in self.engines:
            print(f'{engine.name} - {engine.state}')

    def __repr__(self):
        return f"Department('{self.title}')"


class DepartmentsIterator(Iterator):
    def __init__(self, departments: List[Department]):
        self._departments = departments
        self._n = 0

    def __iter__(self):
        self._n = 0
        return self

    def __next__(self) -> Department:
        if self._n < len(self._departments):
            val = self._departments[self._n]
            self._n += 1
            return val
        else:
            raise StopIteration


class DepartmentsManagement:
    def __init__(self, departments: List[Department]):
        self.departments_iterator = DepartmentsIterator(departments)

    def call(self):
        pass