from typing import List

from lab5.events import Event, EventType
from lab5.strategy import FirePreparationStrategy, LocalThreatPreparationStrategy, PreparationStrategy, \
    FAFirePreparationStrategy, FALocalThreatPreparationStrategy
from lab5.fire_engines import FireEngine, FireEngineSquad, ReadyState


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
        self._strategy: PreparationStrategy
        self._sender = FireEngineSender()

    @property
    def departments(self):
        return self._departments

    @property
    def available_engines(self):
        return len([
            engine
            for department in self.departments
            for engine in department.engines
            if engine.state == ReadyState()
        ])

    def react_to_event(self, event: Event):
        match event.event_type:
            case EventType.FIRE:
                self._strategy = FirePreparationStrategy(self.departments)
            case EventType.LOCAL_THREAT:
                self._strategy = LocalThreatPreparationStrategy(self.departments)
            case EventType.FIRE_FALSE_ALARM:
                self._strategy = FAFirePreparationStrategy(self.departments)
            case EventType.LOCAL_THREAT_FALSE_ALARM:
                self._strategy = FALocalThreatPreparationStrategy(self.departments)

        print(f'available engines: {self.available_engines}')
        squad = self._strategy.request_squad(event)
        self._sender.add_squad(squad)
        self._sender.notify()
        self._sender.remove_squad(squad)


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

    def notify(self):
        for squad in self.squads:
            squad.send()