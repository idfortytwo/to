from time import sleep

from PyQt5 import QtCore
from PyQt5.Qt import (QWidget, QLabel)
from PyQt5.QtCore import QRect, QPoint, QThread, pyqtSignal
from PyQt5.QtGui import QPixmap, QColor, QPainter, QKeyEvent
from PyQt5.QtWidgets import QGridLayout

from lab4.simulation import Simulation
from lab4.states import ImmuneState, VulnerableState, SympthomaticState, AsympthomaticState


class RefreshThread(QThread):
    finished = pyqtSignal()

    def __init__(self, *args, turns_per_second, **kwargs):
        super().__init__(*args, **kwargs)
        self._turns_per_second = turns_per_second
        self._paused = True

    @property
    def paused(self) -> bool:
        return self._paused

    @paused.setter
    def paused(self, value):
        self._paused = value

    def run(self):
        while True:
            if not self.paused:
                sleep(1 / self._turns_per_second)
                if not self.paused:
                    self.finished.emit()  # noqa


class GUI(QWidget):
    def __init__(self, simulation: Simulation, turns_per_second: int = 1):
        super().__init__()
        self._simulation = simulation
        self._area = self._simulation.area
        self._turns_per_second = turns_per_second

        self._area_rect = QRect(0, 0, self._area.n - 1, self._area.m - 1)
        self._state_colors = {
            ImmuneState(): QColor(0, 204, 102),
            VulnerableState(): QColor(0, 0, 0),
            SympthomaticState(): QColor(255, 0, 0),
            AsympthomaticState(): QColor(255, 153, 0)
        }

        self.initUI()

        self._thread = RefreshThread(self, turns_per_second=self._turns_per_second)
        # self._start_refresh_thread()

    def initUI(self):
        self._pop_count_label = QLabel(self)
        self._turn_label = QLabel(self)
        self._sick_count_label = QLabel(self)
        self._sick_count_label.setStyleSheet('QLabel { color: rgb(255, 64, 0) }')
        self._vulnerable_count_label = QLabel(self)
        self._immune_count_label = QLabel(self)
        self._immune_count_label.setStyleSheet('QLabel { color: rgb(0, 204, 102) }')

        self._pixmap_label = QLabel(self)
        self._pixmap = QPixmap(self._area.n, self._area.m)
        self._pixmap_label.setPixmap(self._pixmap)

        grid = QGridLayout(self)
        grid.addWidget(self._pop_count_label, 0, 0)
        grid.addWidget(self._turn_label, 0, 2)
        grid.addWidget(self._vulnerable_count_label, 1, 0)
        grid.addWidget(self._sick_count_label, 1, 1)
        grid.addWidget(self._immune_count_label, 1, 2)
        grid.addWidget(self._pixmap_label, 2, 0, 2, 3)
        self.setLayout(grid)

        self.move(300, 100)
        self.setWindowTitle('Simulation')
        self.show()

    def _start_refresh_thread(self):
        self._thread.start()
        self._thread.finished.connect(lambda: self._next_turn())  # noqa

    def _next_turn(self):
        self._simulation.process()
        self._refresh()

    def _refresh(self):
        self._refresh_pixmap()
        self._refresh_counts()

    def _refresh_counts(self):
        self._turn_label.setText(f'Turn: {self._simulation.turn}')
        self._pop_count_label.setText(f'Population: {self._simulation.pop.total_count}')
        self._vulnerable_count_label.setText(f'Vulnerable: {self._simulation.pop.vulnerable_count}')
        self._sick_count_label.setText(f'Sick: {self._simulation.pop.sick_count}')
        self._immune_count_label.setText(f'Immune: {self._simulation.pop.immune_count}')

    def _refresh_pixmap(self):
        painter = QPainter(self._pixmap)
        painter.fillRect(self._area_rect, QColor(255, 255, 255, 255))
        painter.setPen(QColor(200, 200, 200, 255))
        painter.drawRect(self._area_rect)

        for person, (x, y) in self._simulation.pop.items():
            painter.setPen(self._state_colors[person.state])
            painter.drawPoint(QPoint(round(x), round(y)))

        painter.end()

        self._pixmap_label.setPixmap(self._pixmap.scaledToHeight(500))
        self._pixmap_label.update()

    def keyPressEvent(self, event: QKeyEvent):
        match event.key():
            case QtCore.Qt.Key_Left:
                print('turn <', self._simulation.turn)
                self._simulation.restore(self._simulation.turn - 1)
                self._refresh()
            case QtCore.Qt.Key_Right:
                print('turn >', self._simulation.turn)
                if not self._simulation.restore(self._simulation.turn + 1):
                    self._simulation.process()
                self._refresh()
            case QtCore.Qt.Key_Space:
                pass