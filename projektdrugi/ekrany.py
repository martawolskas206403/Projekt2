from PyQt5 import QtWidgets, QtCore, QtGui
import pyqtgraph as pg

class EkranWizualizacji(QtWidgets.QWidget):
    def __init__(self, system_logic, parent=None):
        super().__init__(parent)
        self.logic = system_logic

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        
        #rysowanie rur i zbiorników
        for rura in self.logic.rury:
            rura.draw(painter)
        for zbiornik in self.logic.zbiorniki:
            zbiornik.draw(painter)
        
        #grzalka
        g_x, g_y = 425, 240
        is_heating = self.logic.rury[1].czy_plynie
        painter.setBrush(QtGui.QColor("#ff6600" if is_heating else "#444"))
        painter.drawRect(g_x, g_y, 40, 20)
        painter.setPen(QtCore.Qt.white)
        painter.drawText(g_x - 10, g_y - 5, f"GRZAŁKA ({self.logic.zadana_temp}°C)")

        #pompa
        p_x, p_y = 550, 545
        is_pumping = self.logic.rury[2].czy_plynie
        painter.setBrush(QtGui.QColor("lime" if is_pumping else "red"))
        painter.drawEllipse(p_x, p_y, 30, 30)
        painter.setPen(QtCore.Qt.white)
        painter.drawText(p_x - 5, p_y - 5, "POMPA")

class EkranWykresow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QtWidgets.QVBoxLayout(self)
        self.graph = pg.PlotWidget()
        self.graph.setBackground('#1a1a1a')
        self.graph.setTitle("Poziom Produktu Z4", color="w")
        self.graph.setLabel('left', 'Napełnienie [%]')
        self.graph.setLabel('bottom', 'Czas')
        self.curve = self.graph.plot(pen=pg.mkPen(color='c', width=2))
        layout.addWidget(self.graph)

    def update_chart(self, data):
        self.curve.setData(data)