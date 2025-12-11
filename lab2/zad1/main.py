import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QSlider, QLabel
from PyQt5.QtCore import Qt, QRectF, QPointF
from PyQt5.QtGui import QPainter, QColor, QBrush, QPen, QPainterPath

class Zbiornik(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        #minimalny rozmiar, aby rysunek sie zmiescil
        self.setMinimumSize(300, 400)

        #parametry geometryczne
        self.top_trapez_h = 60  #wysokosc gornego trapezu
        self.rect_h = 200       #wysokosc srodka
        self.bot_trapez_h = 60  #wysokosc dolnego trapezu

        self.width_top = 200    #szerokosc wlotu
        self.width_mid = 140    #szerokosc srodka
        self.width_bot = 40     #szerokosc wylotu

        #calkowita wysokosc "uzyteczna" zbiornika
        self.total_tank_height = self.top_trapez_h + self.rect_h + self.bot_trapez_h

        # --- Stan poczatkowy ---
        self._poziom = 0.5  # 50% (wartosc od 0.0 do 1.0)
        
        #pozycja rysowania wewnatrz widgetu
        self.draw_x = 50
        self.draw_y = 50

    def setPoziom(self, poziom):
        """ Ustawia poziom cieczy (0.0 - 1.0) i odswieza widok. """
        self._poziom = max(0.0, min(1.0, poziom))
        self.update()  #wymus przerysowanie (wywolaj paintEvent)

    def setPolozenie(self, x, y):
        """ Ustawia pozycje zbiornika wewnatrz widgetu. """
        self.draw_x = x
        self.draw_y = y
        self.update()

    def getPoziom(self):
        """ Zwraca aktualny poziom cieczy. """
        return self._poziom

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 1.obliczamy punkty wzgledem draw_x i draw_y
        cx = self.draw_x + (self.width_top / 2)
        start_y = self.draw_y

        # 2.definiujemy ksztalt zbiornika (sciezka)
        path = QPainterPath()

        #punkty kluczowe (naprawione polamania linii)
        p1_tl = QPointF(cx - self.width_top / 2, start_y)
        p1_tr = QPointF(cx + self.width_top / 2, start_y)
        
        p2_ml = QPointF(cx - self.width_mid / 2, start_y + self.top_trapez_h)
        p2_mr = QPointF(cx + self.width_mid / 2, start_y + self.top_trapez_h)
        
        p3_bl = QPointF(cx - self.width_mid / 2, start_y + self.top_trapez_h + self.rect_h)
        p3_br = QPointF(cx + self.width_mid / 2, start_y + self.top_trapez_h + self.rect_h)
        
        p4_bl = QPointF(cx - self.width_bot / 2, start_y + self.total_tank_height)
        p4_br = QPointF(cx + self.width_bot / 2, start_y + self.total_tank_height)

        #budowanie sciezki (laczenie punktow)
        path.moveTo(p1_tl)
        path.lineTo(p1_tr)
        path.lineTo(p2_mr)
        path.lineTo(p3_br)
        path.lineTo(p4_br)
        path.lineTo(p4_bl)
        path.lineTo(p3_bl)
        path.lineTo(p2_ml)
        path.lineTo(p1_tl)
        path.closeSubpath()

        # 3.rysowanie cieczy (z maskowaniem)
        painter.save()          #zapisz stan malarza
        painter.setClipPath(path)  #ustaw maske przycinania

        liquid_height_px = self.total_tank_height * self._poziom

        rect_liquid = QRectF(
            cx - self.width_top / 2,                          # X (szeroki zapas)
            start_y + self.total_tank_height - liquid_height_px,  # Y poczatku cieczy
            self.width_top,                                   #szerokosc
            liquid_height_px                                  #wysokosc
        )

        #rysujemy prostokat, ktory zostanie przyciety do ksztaltu sciezki
        painter.fillRect(rect_liquid, QColor(0, 120, 255, 180))
        painter.restore()       #usun maskowanie

        # 4.rysowanie OBRYSU (Ramki) na wierzchu
        pen = QPen(Qt.gray, 4)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(path)

# --- Kod testowy aplikacji ---
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    #tworzymy kontener z ukladem, zeby dodac suwak
    main_window = QWidget()
    layout = QVBoxLayout(main_window)
    
    #widget zbiornika
    tank = Zbiornik()
    layout.addWidget(tank)
    
    #etykieta
    label = QLabel("Poziom cieczy:")
    layout.addWidget(label)

    #suwak do sterowania
    slider = QSlider(Qt.Horizontal)
    slider.setRange(0, 100)
    slider.setValue(50)
    
    #funkcja aktualizujaca zbiornik gdy ruszamy suwakiem
    def update_tank(value):
        poziom = value / 100.0
        tank.setPoziom(poziom)
        label.setText(f"Poziom cieczy: {int(poziom * 100)}%")

    slider.valueChanged.connect(update_tank)
    layout.addWidget(slider)

    main_window.setWindowTitle("Symulacja Zbiornika")
    main_window.resize(400, 600)
    main_window.show()
    
    sys.exit(app.exec_())