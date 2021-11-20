from typing import List

from lab5.events import Event, EventType
from lab5.execution import FireStrategy, LocalThreatStrategy
from lab5.fire_engines import FireEngine, FireEngineSquad


class Department:
    def __init__(self, title: str, coords):
        self.title = title
        self.coords = coords
        self.engines: List[FireEngine] = [FireEngine(f'{self.title}-{i}') for i in range(5)]

    def print_state(self):
        for engine in self.engines:
            print(f'{engine.name} - {engine.state}')

    def __repr__(self):
        return f"Department('{self.title}')"


class DepartmentManager:
    def __init__(self, departments: List[Department]):
        self._departments = departments
        self._sender = FireEngineSender()

    @property
    def departments(self):
        return self._departments

    @property
    def sender(self):
        return self._sender

    def react_to_event(self, event: Event):
        match event.event_type:
            case EventType.FIRE:
                self.strategy = FireStrategy(self.departments)
            case EventType.LOCAL_THREAT:
                self.strategy = LocalThreatStrategy(self.departments)

        engines = self.strategy.request_engines(event)

        squad = FireEngineSquad(engines)
        self.sender.add_squad(squad)
        self.sender.send()


class FireEngineSender:
    def __init__(self, squads: List[FireEngineSquad] = None):
        self._squads = squads if squads else []

    @property
    def squads(self):
        return self._squads

    def add_squad(self, squad: FireEngineSquad):
        self.squads.append(squad)

    def remove_squad(self, squad: FireEngineSquad):
        self.squads.remove(squad)

    def send(self):
        for squad in self.squads:
            squad.send()
            self.remove_squad(squad)