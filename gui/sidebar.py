from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel
)

class Sidebar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Menu"))
        layout.addWidget(QPushButton("🏠"))
        layout.addWidget(QPushButton("⬇️"))
        layout.addWidget(QPushButton("♻️"))
        layout.addWidget(QPushButton("⚙️"))
        layout.addStretch()
        self.setLayout(layout)
