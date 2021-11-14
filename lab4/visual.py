import traceback
from time import sleep

from PyQt5.Qt import (QWidget, QLabel)
from PyQt5.QtCore import QRect, QPoint, QThread, pyqtSignal
from PyQt5.QtGui import QPixmap, QColor, QPainter
from PyQt5.QtWidgets import QGridLayout

from lab4.simulation import Simulation
from lab4.states import ImmuneState, VulnerableState, SympthomaticState, AsympthomaticState


class RefreshThread(QThread):
    finished = pyqtSignal()

    def __init__(self, *args, turns_per_second, **kwargs):
        super().__init__(*args, **kwargs)
        self._turns_per_second = turns_per_second

    def run(self):
        while True:
            sleep(1 / self._turns_per_second)
            self.finished.emit()  # noqa


class GUI(QWidget):
    def __init__(self, simulation: Simulation, turns_per_second: int = 1):
        super().__init__()
        self._simulation = simulation
        self._area = self._simulation.area
        self._pop = self._simulation.pop
        self._turns_per_second = turns_per_second

        self._area_rect = QRect(0, 0, self._area.n - 1, self._area.m - 1)
        self._state_colors = {
            ImmuneState(): QColor(0, 204, 102),
            VulnerableState(): QColor(0, 0, 0),
            SympthomaticState(): QColor(255, 0, 0),
            AsympthomaticState(): QColor(255, 153, 0)
        }

        self.initUI()

    def initUI(self):
        self._pop_count_label = QLabel(self)
        self._sick_count_label = QLabel(self)
        self._vulnerable_count_label = QLabel(self)
        self._immune_count_label = QLabel(self)

        self._pixmap_label = QLabel(self)
        self._pixmap = QPixmap(self._area.n, self._area.m)
        self._pixmap_label.setPixmap(self._pixmap)

        self._redraw_pixmap()

        grid = QGridLayout(self)
        grid.addWidget(self._pop_count_label, 0, 0)
        grid.addWidget(self._pixmap_label, 1, 0)
        self.setLayout(grid)

        self.move(300, 100)
        self.setWindowTitle('Simulation')

        self._start_refresh_thread()
        self.show()

    def _start_refresh_thread(self):
        thread = RefreshThread(self, turns_per_second=self._turns_per_second)
        thread.start()
        thread.finished.connect(lambda: self.refresh())  # noqa

    def refresh(self):
        try:
            self._refresh_pop_count()
            self._redraw_pixmap()
            self._simulation.process()
        except:  # noqa
            traceback.print_exc()
            exit()

    def _refresh_pop_count(self):
        self._pop_count_label.setText(f'Population: {self._pop.total_count}')

    def _redraw_pixmap(self):
        painter = QPainter(self._pixmap)
        painter.fillRect(self._area_rect, QColor(255, 255, 255, 255))
        painter.setPen(QColor(200, 200, 200, 255))
        painter.drawRect(self._area_rect)

        for person, (x, y) in self._pop.items():
            painter.setPen(self._state_colors[person.state])
            painter.drawPoint(QPoint(round(x), round(y)))

        painter.end()

        self._pixmap_label.setPixmap(self._pixmap.scaledToHeight(500))
        self._pixmap_label.update()
