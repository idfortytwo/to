import sys

from PyQt5.QtWidgets import QApplication

from lab4.visual import GUI
from simulation import Simulation

sim = Simulation(n=50, m=50, starting_pop_count=100,
                 grow_count=10, grow_p=0.2)

sim2 = Simulation(n=50, m=50, starting_pop_count=2,
                  grow_count=1, grow_p=1)

app = QApplication(sys.argv)
ex = GUI(sim, turns_per_second=25, preload_turns=50)
sys.exit(app.exec_())
