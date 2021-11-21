import time

from lab5.departments import DepartmentManager, Department
from lab5.events import Event, EventType

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
# print(departments)

SKKM = DepartmentManager(departments)
fire_1 = Event(EventType.FIRE, (50, 20))
local_threat_1 = Event(EventType.LOCAL_THREAT, (50, 19.8))
local_threat_2 = Event(EventType.LOCAL_THREAT, (50, 19.8))
fire_3 = Event(EventType.FIRE, (50, 19.8))

SKKM.react_to_event(fire_1)
time.sleep(1)
SKKM.react_to_event(local_threat_1)
time.sleep(1)
SKKM.react_to_event(local_threat_2)
time.sleep(1)
SKKM.react_to_event(fire_3)

# cei = ClosestEnginesIterator(departments, ev)
# for en in cei:
#     print(en)