import sys

from PyQt5.QtWidgets import QApplication

from lab4.visual import GUI
from simulation import Simulation

params = {
    'n': 50,
    'm': 50,
    'starting_pop_count': 300,
    'grow_count': 10,
    'grow_p': 0.3
}
sim_no_immune = Simulation(**params, immune_p=0)
sim_immune = Simulation(**params, immune_p=0.2)

app = QApplication(sys.argv)
ex = GUI(sim_no_immune, turns_per_second=25, preload_turns=500)
# print('ex1 ready')
# ex2 = GUI(sim_immune, turns_per_second=25, preload_turns=100)
sys.exit(app.exec_())