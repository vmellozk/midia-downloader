from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QPushButton, QLabel, QVBoxLayout
)
from PySide6.QtCore import Signal

class Sidebar(QWidget):
    change_scr = Signal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout()
        layout.addStretch()
        home_btn = QPushButton("🏠")
        settings_btn = QPushButton("⚙️")
        layout.addWidget(home_btn)
        layout.addWidget(settings_btn)
        layout.addStretch()
        self.setLayout(layout)
        
        # Conetando ao Signal de cada botão
        home_btn.clicked.connect(lambda: self.change_scr.emit("home"))
        settings_btn.clicked.connect(lambda: self.change_scr.emit("settings"))

class HomeScreen(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel())
        self.setLayout(layout)
        
class SettingsScreen(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Configurações"))
        self.setLayout(layout)
