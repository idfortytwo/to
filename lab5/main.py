import random
import time

from typing import List

from lab5.departments import DepartmentManager, Department
from lab5.events import Event, EventType


class Simulator:
    def __init__(self, departments: List[Department]):
        self.SKKM = DepartmentManager(departments)

    @staticmethod
    def create_event() -> Event:
        x = random.uniform(49.95855025648945,  50.154564013341733)
        y = random.uniform(19.688292482742395, 20.02470275868902)

        event_type = EventType.LOCAL_THREAT if random.random() < 0.7 else EventType.FIRE
        if random.random() < 0.05:
            event_type = EventType.LOCAL_THREAT_FALSE_ALARM if event_type == EventType.LOCAL_THREAT \
                else EventType.FIRE_FALSE_ALARM

        return Event(event_type, (x, y))

    def run(self):
        while True:
            event = self.create_event()
            self.SKKM.react_to_event(event)
            time.sleep(0.5)


def main():
    departments = [
        Department('JRG Szkoły Aspirantów PSP', (50.07735, 20.03269)),
        Department('JRG Skawina', (49.97218, 19.79603)),
        Department('LSP Lotniska w Balinach', (50.07311, 19.78584)),
        Department('JRG-1', (50.05995, 19.94324)),
        Department('JRG-2', (50.03352, 19.93583)),
        Department('JRG-3', (50.07560, 19.88730)),
        Department('JRG-4', (50.03758, 20.00538)),
        Department('JRG-5', (50.09174, 19.91967)),
        Department('JRG-6', (50.01594, 20.01529)),
        Department('JRG-7', (50.09412, 19.97739))
    ]
    simulator = Simulator(departments)
    simulator.run()


if __name__ == '__main__':
    main()