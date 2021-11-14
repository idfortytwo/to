import math
import random

from typing import Dict, Tuple

from lab4.states import Person, VulnerableState, SympthomaticState, AsympthomaticState


class Area:
    def __init__(self, n: int, m: int, starting_pop_count: int, grow_count: int, grow_p: float):
        self._n = n
        self._m = m
        self._starting_pop_count = starting_pop_count
        self._grow_count = grow_count
        self._grow_p = grow_p
        self.pop: Dict[Person, Tuple[float, float]] = self.generate_pop()

    @property
    def n(self):
        return self._n

    @property
    def m(self):
        return self._m

    @property
    def pop_count(self):
        return len(self.pop)

    def generate_pop(self) -> Dict[Person, Tuple[float, float]]:
        return {
            Person(VulnerableState()): (random.randrange(0, self.n), random.randrange(0, self.m))
            for _
            in range(self._starting_pop_count)
        }

    def process(self):
        self._move_people()
        self._add_people()
        self._check_proximity()

    @staticmethod
    def _gen_vector():
        angle = random.random() * 2 * math.pi
        distance = random.random() * 2.5
        return angle, distance

    def _move_people(self):
        to_delete = []

        for person, (x, y) in self.pop.items():
            person.poke()

            angle, distance = self._gen_vector()
            new_x = x + math.sin(angle) * distance
            new_y = y + math.cos(angle) * distance

            if new_x <= 0 or new_x >= self.n or new_y <= 0 or new_y >= self.m:
                if random.random() < 0.5:
                    to_delete.append(person)
                    continue
                else:
                    new_x = x - math.sin(angle) * distance
                    new_y = y - math.cos(angle) * distance

            self.pop[person] = (new_x, new_y)

        for person in to_delete:
            del self.pop[person]

    def _gen_border_loc(self):
        horizontal_loc = random.getrandbits(1)
        if horizontal_loc:
            starting_point = (random.randrange(0, self.n), random.choice([0, self.n]))
        else:
            starting_point = (random.choice([0, self.n]), random.randrange(0, self.n))
        return starting_point

    @staticmethod
    def _gen_newcomer_state():
        if random.random() < 0.1:
            if random.getrandbits(1):
                state = SympthomaticState()
            else:
                state = AsympthomaticState()
        else:
            state = VulnerableState()
        return state

    def _add_people(self):
        for _ in range(self._grow_count):
            if random.random() < self._grow_p:
                starting_point = self._gen_border_loc()
                state = self._gen_newcomer_state()
                self.pop.update({Person(state): starting_point})

    def _check_proximity(self):
        for p1, (x1, y1) in self.pop.items():
            for p2, (x2, y2) in self.pop.items():
                if p1 != p2:
                    distance = math.sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1))
                    if distance <= 2:
                        p1.contact(p2)


class PopStat:
    def __init__(self, pop):
        self._pop = pop

    @property
    def pop_count(self):
        return len(self._pop)