MAIN_STYLE = """
    QMainWindow { background-color: #222; }
    QTabWidget::pane { border: 1px solid #444; background: #222; }
    QTabBar::tab { background: #333; color: white; padding: 12px; min-width: 150px; }
    QTabBar::tab:selected { background: #0078d7; font-weight: bold; }
    QGroupBox { color: #00e5ff; font-weight: bold; border: 1px solid #555; }
    QLabel { color: white; font-weight: bold; }
    QLineEdit { background: #000; color: #0f0; border: 1px solid #555; padding: 3px; }
"""

def get_status_style(state):
    styles = {
        "ALARM": "background-color: red; color: white; font-weight: bold;",
        "PRACA": "background-color: green; color: white; font-weight: bold;",
        "IDLE": "background-color: #333; color: white;"
    }
    return styles.get(state, styles["IDLE"])