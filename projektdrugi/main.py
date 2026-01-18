import sys
from PyQt5 import QtWidgets, QtCore
from gui import ScadaGui
from logic import ProcessLogic
import styles

class AppController(ScadaGui):
    def __init__(self):
        self.proc = ProcessLogic()
        super().__init__(self.proc)
        self.is_running = False
        self.history = []
        
        # podpiecie sygnalow pod przyciski z gui
        self.btn_start.clicked.connect(self.toggle)
        self.btn_reset.clicked.connect(self.reset)
        
        # odswiezenie aplikacji co 50ms
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_simulation)

    def toggle(self):
        if not self.is_running:
            try:
                #pobieranie danych z pol tekstowych
                lvl = float(self.input_level.text())
                target = float(self.input_target.text())
                spd = float(self.input_speed.text())
                tmp = int(self.input_temp.text())

                #walidacja danych wejsciowych
                errors = []
                if not (0 <= lvl <= 100): errors.append("Poziom Z1 (0-100)")
                if not (0 <= target <= 100): errors.append("Cel (0-100)")
                if not (0 <= spd <= 10): errors.append("Szybkość (0-10)")
                
                if errors:
                    self.status_label.setText(f"BŁĄD: {', '.join(errors)}")
                    self.status_label.setStyleSheet("background-color: red; color: white;")
                    return 

                #logika startu jesli system jest pusty inicjalizujemy z1 i z2
                suma_wszystkich = sum(z.poziom for z in self.proc.zbiorniki)
                if suma_wszystkich < 0.5:
                    self.proc.z1.poziom = lvl
                    #bufor dostaje to czego brakuje w z1 do pełna aby zawsze było z czego dobrać różnicę do celu
                    self.proc.z2.poziom = 100.0 - lvl 
                
                # pzypisanie parametrow do logiki procesowej
                self.proc.cel_produktu = target
                self.proc.speed = spd
                self.proc.zadana_temp = tmp
                
                #zmiana wygladu przycisu
                self.is_running = True
                self.timer.start(50)
                self.btn_start.setText("STOP")
                self.btn_start.setStyleSheet("background-color: red; color: white; font-weight: bold;")
            except ValueError:
                self.status_label.setText("BŁĄD: WPISZ LICZBY")
                self.status_label.setStyleSheet("background-color: red; color: white;")
        else:
            #zatrzymanie symulacji
            self.is_running = False
            self.timer.stop()
            self.btn_start.setText("WZNÓW")
            self.btn_start.setStyleSheet("background-color: green; color: white; font-weight: bold;")
            for r in self.proc.rury: r.czy_plynie = False

    def reset(self):
        #powrot do stanu poczatkowego
        self.timer.stop()
        self.is_running = False
        self.proc = ProcessLogic()
        self.history = []
        self.charts.update_chart([])
        self.viz.logic = self.proc
        self.btn_start.setText("START")
        self.btn_start.setStyleSheet("background-color: green; color: white; font-weight: bold;")
        self.status_label.setText("ZRESETOWANO")
        self.status_label.setStyleSheet(styles.get_status_style("IDLE"))
        self.viz.update()

    def update_simulation(self):
        self.proc.calculate_step()
        
        # sprawdzenie stanow specjalnych
        gotowe = self.proc.z4.poziom >= self.proc.cel_produktu
        alarm = self.proc.has_alarm()
        
        if gotowe:
            state = "IDLE"
            msg = f"ZAKOŃCZONO: Osiągnięto {int(self.proc.z4.poziom)}%"
            self.is_running = False
            self.timer.stop()
            self.btn_start.setText("START")
            for r in self.proc.rury: r.czy_plynie = False
        elif alarm:
            state = "ALARM"
            msg = "!!! ALARM !!!"
        else:
            state = "PRACA"
            msg = f"PRACA | CEL: {int(self.proc.cel_produktu)}% | T: {self.proc.zadana_temp}°C"
        
        #aktualizacja paska statusu
        self.status_label.setText(msg)
        self.status_label.setStyleSheet(styles.get_status_style(state))
        
        #aktualizacja wykresu
        self.history.append(self.proc.z4.poziom)
        if len(self.history) > 100: self.history.pop(0)
        self.charts.update_chart(self.history)
        
        self.viz.update()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = AppController()
    window.show()
    sys.exit(app.exec_())