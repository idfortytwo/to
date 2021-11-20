from lab5.departments import DepartmentsManagement, Department
from lab5.events import Event, EventType

departments = [
    Department('JRG Szkoły Aspirantów PSP'),
    Department('JRG Skawina'),
    Department('JRG Lotniska w Balinach'),
    *(Department(f'JRG-{i}') for i in range(1, 8))
]
# print(departments)

SKKM = DepartmentsManagement(departments)

d_it = iter(SKKM.departments_iterator)
next(d_it)
d = next(d_it)
d.print_state()

ev = Event(EventType.FIRE, (50, 20))