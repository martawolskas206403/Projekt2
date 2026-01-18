from PyQt5 import QtCore, QtGui

class Zbiornik:
    def __init__(self, x, y, nazwa=""):
        self.x, self.y = x, y
        self.w, self.h = 90, 130
        self.nazwa = nazwa
        self.poziom = 0.0
        
    def draw(self, painter):
        if self.poziom > 0.5:
            h_cieczy = (self.h * self.poziom) / 100.0
            painter.setBrush(QtGui.QColor(0, 120, 255, 200))
            painter.setPen(QtCore.Qt.NoPen)
            painter.drawRect(int(self.x + 2), int(self.y + self.h - h_cieczy), int(self.w - 4), int(h_cieczy))
       
        painter.setPen(QtGui.QPen(QtCore.Qt.white, 3))
        painter.setBrush(QtCore.Qt.NoBrush)
        painter.drawRect(self.x, self.y, self.w, self.h)
        painter.setPen(QtGui.QPen(QtCore.Qt.cyan))
        painter.drawText(self.x, self.y - 10, f"{self.nazwa}: {int(self.poziom)}%")

    def punkt_wejscia_gora(self): return (self.x + self.w // 2, self.y)
    def punkt_wyjscia_dol(self): return (self.x + self.w // 2, self.y + self.h)