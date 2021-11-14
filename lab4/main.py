import sys

from PyQt5.QtWidgets import QApplication

from lab4.visual import GUI
from simulation import Simulation

sim = Simulation(n=100, m=100, starting_pop_count=75,
                 grow_count=3, grow_p=0.5)

app = QApplication(sys.argv)
ex = GUI(sim, turns_per_second=5)
sys.exit(app.exec_())
