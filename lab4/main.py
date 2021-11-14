import sys

from PyQt5.QtWidgets import QApplication

from lab4.states import Person, SympthomaticState, AsympthomaticState
from lab4.visual import GUI
from simulation import Area


area = Area(n=100, m=100, starting_pop_count=20,
            grow_count=1, grow_p=0.5)
# area = Area(100, 100, 0, 0)
# area.pop.update({
#     Person(AsympthomaticState()): (50, 50)
# })
# print(area)
# for person, location in area.pop.items():
#     print(person, location)
# print('')

app = QApplication(sys.argv)
ex = GUI(area)
sys.exit(app.exec_())

# area.process()
# for person, location in area.pop.items():
#     print(person, location)
