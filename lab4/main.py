import sys

from PyQt5.QtWidgets import QApplication

from lab4.visual import GUI
from simulation import Simulation

sim = Simulation(n=50, m=50, starting_pop_count=200,
                 grow_count=10, grow_p=0.2, immune_p=0.1)

sim2 = Simulation(n=50, m=50, starting_pop_count=200,
                  grow_count=10, grow_p=0.2, immune_p=0.0)

app = QApplication(sys.argv)
# ex = GUI(sim, turns_per_second=25, preload_turns=50)
ex = GUI(sim2, turns_per_second=25, preload_turns=300)
sys.exit(app.exec_())
