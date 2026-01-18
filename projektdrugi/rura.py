from PyQt5 import QtCore, QtGui

class Rura:
    def __init__(self, punkty, grubosc=12):
        self.punkty = [QtCore.QPointF(p[0], p[1]) for p in punkty]
        self.grubosc = grubosc
        self.czy_plynie = False

    def draw(self, painter):
        path = QtGui.QPainterPath()
        path.moveTo(self.punkty[0])
        for p in self.punkty[1:]:
            path.lineTo(p)
        painter.setPen(QtGui.QPen(QtGui.QColor("#333"), self.grubosc, QtCore.Qt.SolidLine, QtCore.Qt.FlatCap, QtCore.Qt.RoundJoin))
        painter.drawPath(path)
        if self.czy_plynie:
            painter.setPen(QtGui.QPen(QtGui.QColor(0, 150, 255), self.grubosc - 4, QtCore.Qt.SolidLine, QtCore.Qt.FlatCap, QtCore.Qt.RoundJoin))
            painter.drawPath(path)