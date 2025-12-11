import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QSlider, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt, QRectF, QPointF
from PyQt5.QtGui import QPainter, QColor, QBrush, QPen, QPainterPath

# --- klasa zbiornik z poprzedniego zadania ---
class Zbiornik(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setMinimumSize(300, 400)
        
        #parametry
        self.top_trapez_h = 60
        self.rect_h = 200
        self.bot_trapez_h = 60
        self.width_top = 200
        self.width_mid = 140
        self.width_bot = 40
        self.total_tank_height = self.top_trapez_h + self.rect_h + self.bot_trapez_h
        
        #stan
        self._poziom = 0.5
        self.draw_x = 50
        self.draw_y = 50

    def setPoziom(self, poziom):
        self._poziom = max(0.0, min(1.0, poziom))
        self.update()

    def setPolozenie(self, x, y):
        self.draw_x = x
        self.draw_y = y
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        cx = self.draw_x + (self.width_top / 2)
        start_y = self.draw_y
        
        path = QPainterPath()
        p1_tl = QPointF(cx - self.width_top/2, start_y)
        p1_tr = QPointF(cx + self.width_top/2, start_y)
        p2_ml = QPointF(cx - self.width_mid/2, start_y + self.top_trapez_h)
        p2_mr = QPointF(cx + self.width_mid/2, start_y + self.top_trapez_h)
        p3_bl = QPointF(cx - self.width_mid/2, start_y + self.top_trapez_h + self.rect_h)
        p3_br = QPointF(cx + self.width_mid/2, start_y + self.top_trapez_h + self.rect_h)
        p4_bl = QPointF(cx - self.width_bot/2, start_y + self.total_tank_height)
        p4_br = QPointF(cx + self.width_bot/2, start_y + self.total_tank_height)

        path.moveTo(p1_tl)
        path.lineTo(p1_tr); path.lineTo(p2_mr); path.lineTo(p3_br)
        path.lineTo(p4_br); path.lineTo(p4_bl); path.lineTo(p3_bl)
        path.lineTo(p2_ml); path.lineTo(p1_tl)
        path.closeSubpath()

        painter.save()
        painter.setClipPath(path)
        liquid_h = self.total_tank_height * self._poziom
        rect_liq = QRectF(cx - self.width_top/2, start_y + self.total_tank_height - liquid_h, self.width_top, liquid_h)
        painter.fillRect(rect_liq, QColor(0, 120, 255, 180))
        painter.restore()

        pen = QPen(Qt.gray, 4)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(path)

# --- Zadanie 2 i 3: klasa testująca (główne okno) ---
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dwa Zbiorniki (Zadanie 2 i 3)")
        self.resize(700, 600) #zwiekszona szerokosc dla dwoch zbiornikow

        #glowny uklad pionowy (layout calego okna)
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # 1.uklad POZIOMY dla zbiorników (aby byly obok siebie)
        tanks_layout = QHBoxLayout()
        
        # --- ZBIORNIK 1 ---
        self.zbiornik1 = Zbiornik()
        self.zbiornik1.setStyleSheet("background-color: #222;") # Ciemne tlo
        self.zbiornik1.setPolozenie(20, 30) # Przesuniecie startowe
        tanks_layout.addWidget(self.zbiornik1)

        # --- ZBIORNIK 2 ---
        self.zbiornik2 = Zbiornik()
        self.zbiornik2.setStyleSheet("background-color: #222;") #ciemne tlo
        self.zbiornik2.setPolozenie(20, 30) #przesuniecie startowe
        tanks_layout.addWidget(self.zbiornik2)

        #dodajemy uklad zbiornikow do glownego ukladu
        main_layout.addLayout(tanks_layout)

        # 2.sekcja sterowania (Suwaki i Etykiety)
        
        # --- Sterowanie Zbiornik 1 ---
        self.label1 = QLabel("Poziom Zbiornik 1: 50%")
        self.label1.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.label1)

        self.slider1 = QSlider(Qt.Horizontal)
        self.slider1.setRange(0, 100)
        self.slider1.setValue(50)
        self.slider1.valueChanged.connect(self.zmien_poziom_1)
        main_layout.addWidget(self.slider1)

        #separator
        main_layout.addSpacing(20)

        # --- Sterowanie Zbiornik 2 ---
        self.label2 = QLabel("Poziom Zbiornik 2: 50%")
        self.label2.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.label2)

        self.slider2 = QSlider(Qt.Horizontal)
        self.slider2.setRange(0, 100)
        self.slider2.setValue(50)
        self.slider2.valueChanged.connect(self.zmien_poziom_2)
        main_layout.addWidget(self.slider2)

    def zmien_poziom_1(self, value):
        #przeliczamy 0-100 na float 0.0-1.0
        poziom_float = value / 100.0
        self.zbiornik1.setPoziom(poziom_float)
        self.label1.setText(f"Poziom Zbiornik 1: {value}%")

    def zmien_poziom_2(self, value):
        #przeliczamy 0-100 na float 0.0-1.0
        poziom_float = value / 100.0
        self.zbiornik2.setPoziom(poziom_float)
        self.label2.setText(f"Poziom Zbiornik 2: {value}%")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())