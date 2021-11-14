from __future__ import annotations

import random
from abc import ABC, abstractmethod


class State(ABC):
    @property
    def person(self) -> Person:
        return self._person

    @person.setter
    def person(self, person: Person) -> None:
        self._person = person

    @abstractmethod
    def handle_immune(self) -> None:
        pass

    @abstractmethod
    def handle_vulnerable(self) -> None:
        pass

    @abstractmethod
    def handle_sympthomatic(self) -> None:
        pass

    @abstractmethod
    def handle_asympthomatic(self) -> None:
        pass

    def __eq__(self, other):
        if isinstance(other, State):
            return self.__class__ == other.__class__
        return False

    def __hash__(self):
        return hash(self.__class__)


class ImmuneState(State):
    def handle_immune(self) -> None:
        pass

    def handle_vulnerable(self) -> None:
        pass

    def handle_sympthomatic(self) -> None:
        pass

    def handle_asympthomatic(self) -> None:
        pass

    def __str__(self):
        return 'Immune'


class VulnerableState(State):
    def handle_immune(self) -> None:
        pass

    def handle_vulnerable(self) -> None:
        pass

    def handle_sympthomatic(self) -> None:
        self.person.transition_to(SympthomaticState())

    def handle_asympthomatic(self) -> None:
        self.person.transition_to(AsympthomaticState())

    def __str__(self):
        return 'Vulnerable'


class SympthomaticState(State):
    def handle_immune(self) -> None:
        self.person.transition_to(ImmuneState())

    def handle_vulnerable(self) -> None:
        pass

    def handle_sympthomatic(self) -> None:
        pass

    def handle_asympthomatic(self) -> None:
        pass

    def __str__(self):
        return 'Sympthomatic'


class AsympthomaticState(State):
    def handle_immune(self) -> None:
        self.person.transition_to(ImmuneState())

    def handle_vulnerable(self) -> None:
        pass

    def handle_sympthomatic(self) -> None:
        pass

    def handle_asympthomatic(self) -> None:
        pass

    def __str__(self):
        return 'Asympthomatic'


class Person:
    def __init__(self, state: State) -> None:
        self.transition_to(state)
        self._days_since_contracted = 0
        self._days_to_recover = random.randrange(20, 31)

    @property
    def state(self):
        return self._state

    def transition_to(self, state: State):
        self._state = state
        self._state._person = self

    def request_immune(self):
        self._state.handle_immune()

    def request_vulnerable(self):
        self._state.handle_vulnerable()

    def request_sympthomatic(self):
        self._state.handle_sympthomatic()

    def request_asympthomatic(self):
        self._state.handle_asympthomatic()

    def _get_sick(self):
        if random.getrandbits(1):
            self.request_sympthomatic()
        else:
            self.request_asympthomatic()

    def contact(self, other: Person):
        match other._state:
            case SympthomaticState():
                self._get_sick()
            case AsympthomaticState():
                if random.getrandbits(1):
                    self._get_sick()

    def poke(self):
        if self._state in [SympthomaticState(), AsympthomaticState()]:
            self._days_since_contracted += 1

        if self._days_since_contracted >= self._days_to_recover:
            self.request_immune()

    def __repr__(self):
        return f'Person(\'{self._state}\')'