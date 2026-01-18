from PyQt5 import QtWidgets, QtCore
from ekrany import EkranWizualizacji, EkranWykresow
import styles

class ScadaGui(QtWidgets.QMainWindow):
    def __init__(self, logic):
        super().__init__()
        self.logic = logic
        self.setWindowTitle("System SCADA - Kontrola Produkcji")
        self.setFixedSize(1000, 850)
        self.setStyleSheet(styles.MAIN_STYLE)
        
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        layout = QtWidgets.QVBoxLayout(central)

        ctrl_box = QtWidgets.QGroupBox("Kontrola Procesu")
        ctrl_layout = QtWidgets.QHBoxLayout()
        ctrl_layout.setContentsMargins(15, 25, 15, 15)
        
        self.input_level = QtWidgets.QLineEdit("100")
        self.input_target = QtWidgets.QLineEdit("100")
        self.input_speed = QtWidgets.QLineEdit("0.8")
        self.input_temp = QtWidgets.QLineEdit("60")
        self.btn_start = QtWidgets.QPushButton("START")
        self.btn_reset = QtWidgets.QPushButton("RESET")
        
        for w in [QtWidgets.QLabel("Z1 (%):"), self.input_level, 
                  QtWidgets.QLabel("CEL (%):"), self.input_target, 
                  QtWidgets.QLabel("V:"), self.input_speed, 
                  QtWidgets.QLabel("T:"), self.input_temp, 
                  self.btn_start, self.btn_reset]:
            ctrl_layout.addWidget(w)
        ctrl_box.setLayout(ctrl_layout)
        
        self.tabs = QtWidgets.QTabWidget()
        self.viz = EkranWizualizacji(self.logic)
        self.charts = EkranWykresow()
        self.tabs.addTab(self.viz, "WIZUALIZACJA")
        self.tabs.addTab(self.charts, "WYKRESY")
        
        self.status_label = QtWidgets.QLabel(" STATUS: GOTOWY ")
        self.status_label.setAlignment(QtCore.Qt.AlignCenter)
        self.status_label.setMinimumHeight(40)
        self.statusBar().addPermanentWidget(self.status_label, 1)
        
        layout.addWidget(ctrl_box)
        layout.addWidget(self.tabs)