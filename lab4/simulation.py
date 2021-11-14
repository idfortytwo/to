import itertools
import math
import random
from collections import UserDict, defaultdict
from typing import Tuple, DefaultDict

from lab4.states import Person, VulnerableState, SympthomaticState, AsympthomaticState, ImmuneState


class Population(UserDict):
    _vulnerable = VulnerableState()
    _immune = ImmuneState()
    _sympthomatic = SympthomaticState()
    _asympthomatic = AsympthomaticState()

    def generate_starting(self, n, m, count):
        self.update({
            Person(VulnerableState()): (random.randrange(0, n), random.randrange(0, m))
            for _
            in range(count)
        })

    @property
    def total_count(self):
        return len(self)

    @property
    def vulnerable_count(self):
        return len(list(filter(lambda p: p.state == self._vulnerable, self)))

    @property
    def sick_count(self):
        return len(list(filter(lambda p: p.state in [self._sympthomatic, self._asympthomatic], self)))

    @property
    def immune_count(self):
        return len(list(filter(lambda p: p.state == self._immune, self)))


class Area:
    def __init__(self, n: int, m: int):
        self._n = n
        self._m = m

    @property
    def n(self):
        return self._n

    @property
    def m(self):
        return self._m


class Simulation:
    def __init__(self, n: int, m: int, starting_pop_count: int, grow_count: int, grow_p: float):
        self._area = Area(n, m)
        self._starting_pop_count = starting_pop_count
        self._grow_count = grow_count
        self._grow_p = grow_p

        self._pop: Population[Person, Tuple[float, float]] = Population()
        self._pop.generate_starting(n, m, starting_pop_count)

        self._prev_contacts: DefaultDict[Tuple[Person, Person], int] = defaultdict(int)
        self._curr_contacts: DefaultDict[Tuple[Person, Person], int] = defaultdict(int)

        self.count = 0

    @property
    def area(self):
        return self._area

    @property
    def pop(self):
        return self._pop

    def process(self):
        self._move_people()
        self._add_people()
        self._check_proximity()
        self._check_contacts()

        # self._test_comb()
        # for k, v in self._curr_contacts.items():
        #     print(k, v)
        # exit()

    @staticmethod
    def _gen_vector():
        angle = random.random() * 2 * math.pi
        distance = random.random() * 2.5
        return angle, distance

    def _move_people(self):
        to_delete = []

        for person, (x, y) in self._pop.items():
            person.poke()

            angle, distance = self._gen_vector()
            new_x = x + math.sin(angle) * distance
            new_y = y + math.cos(angle) * distance

            if new_x <= 0 or new_x >= self.area.n or new_y <= 0 or new_y >= self.area.m:
                if random.random() < 0.5:
                    to_delete.append(person)
                    continue
                else:
                    new_x = x - math.sin(angle) * distance
                    new_y = y - math.cos(angle) * distance

            self._pop[person] = (new_x, new_y)

        for person in to_delete:
            del self._pop[person]

    def _gen_border_loc(self):
        horizontal_loc = random.getrandbits(1)
        if horizontal_loc:
            starting_point = (random.randrange(0, self.area.n), random.choice([0, self.area.n]))
        else:
            starting_point = (random.choice([0, self.area.n]), random.randrange(0, self.area.n))
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
                self._pop.update({Person(state): starting_point})

    def _check_proximity(self):
        for ((p1, (x1, y1)), (p2, (x2, y2))) in itertools.combinations(self._pop.items(), 2):
            distance = math.sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1))
            if distance <= 2:
                self._curr_contacts[(p1, p2)] += 1
            else:
                self._curr_contacts[(p1, p2)] = 0

    def _check_contacts(self):
        pairs_to_delete = []

        for (_, prev_duration), ((p1, p2), curr_duration) \
                in zip(self._prev_contacts.items(), self._curr_contacts.items()):
            if curr_duration >= 3:  # noqa
                p1.contact(p2)
                p2.contact(p1)
                pairs_to_delete.append((p1, p2))
            elif prev_duration == curr_duration:
                pairs_to_delete.append((p1, p2))

        for pair in pairs_to_delete:
            del self._curr_contacts[pair]

        self._prev_contacts = self._curr_contacts.copy()