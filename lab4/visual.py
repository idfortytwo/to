import traceback
from time import sleep

from PyQt5.Qt import (QWidget, QHBoxLayout, QLabel)
from PyQt5.QtCore import QRect, QPoint, QThread, pyqtSignal
from PyQt5.QtGui import QPixmap, QColor, QPainter, QBrush
from PyQt5.QtWidgets import QVBoxLayout, QGridLayout

from lab4.simulation import Area, PopStat
from lab4.states import ImmuneState, VulnerableState, SympthomaticState, AsympthomaticState


class RefreshThread(QThread):
    finished = pyqtSignal()

    def run(self):
        while True:
            sleep(1 / 25)
            self.finished.emit()  # noqa


class GUI(QWidget):
    def __init__(self, area: Area):
        super().__init__()
        self._area = area
        self._area_rect = QRect(0, 0, self._area.n - 1, self._area.m - 1)
        self._state_colors = {
            ImmuneState(): QColor(0, 204, 102),
            VulnerableState(): QColor(0, 0, 0),
            SympthomaticState(): QColor(255, 0, 0),
            AsympthomaticState(): QColor(255, 153, 0)
        }
        self._pop_stat = PopStat(self._area.pop)

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
        thread = RefreshThread(self)
        thread.start()
        thread.finished.connect(lambda: self.refresh())  # noqa

    def refresh(self):
        try:
            self._refresh_pop_count()
            self._redraw_pixmap()
            self._area.process()
        except Exception as e:
            traceback.print_exc(e)

    def _refresh_pop_count(self):
        pop_count = self._pop_stat.pop_count
        self._pop_count_label.setText(f'Population: {pop_count}')

    def _redraw_pixmap(self):
        painter = QPainter(self._pixmap)
        painter.fillRect(self._area_rect, QColor(255, 255, 255, 255))
        painter.drawRect(self._area_rect)

        for person, (x, y) in self._area.pop.items():
            painter.setPen(self._state_colors[person.state])
            painter.drawPoint(QPoint(round(x), round(y)))

        painter.end()

        self._pixmap_label.setPixmap(self._pixmap.scaledToHeight(500))
        self._pixmap_label.update()
