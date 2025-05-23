from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QPushButton, QLabel
)

class Sidebar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout()
        layout.addStretch()
        layout.addWidget(QPushButton("🏠"))
        layout.addWidget(QPushButton("⬇️"))
        layout.addWidget(QPushButton("♻️"))
        layout.addWidget(QPushButton("⚙️"))
        layout.addStretch()
        self.setLayout(layout)
