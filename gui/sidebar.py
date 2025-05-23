from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QPushButton, QLabel,
    QVBoxLayout, QComboBox, QCheckBox, QLineEdit,
    QFileDialog
)
from PySide6.QtCore import Signal, Qt

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
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # Título
        title = QLabel("Configurações do Aplicativo")
        title.setStyleSheet("font-size: 18pt; font-weight: bold;")
        layout.addWidget(title)
        
        # Seção: Idioma
        layout.addWidget(QLabel("Idioma"))
        self.language_combo = QComboBox()
        self.language_combo.addItems(["Português (PT-BR)", "English (EN)", "Español"])
        layout.addWidget(self.language_combo)
        
        # Seção: Tema
        layout.addWidget(QLabel("Tema"))
        self.theme_checkbox = QCheckBox("Ativar modo escuro")
        layout.addWidget(self.theme_checkbox)
        
        # Seção: Caminho Padrão de Download
        layout.addWidget(QLabel("Pasta de download padrão"))
        path_layout = QHBoxLayout()
        self.path_input = QLineEdit()
        self.path_button = QPushButton("Selecionar pasta")
        self.path_button.clicked.connect(self.select_folder)
        path_layout.addWidget(self.path_input)
        path_layout.addWidget(self.path_button)
        layout.addLayout(path_layout)
        
        # Seção: Preferências
        self.auto_open_checkbox = QCheckBox("Abrir pasta após o download")
        layout.addWidget(self.auto_open_checkbox)
        
        # Botão de Salvar
        save_button = QPushButton("Salvar configurações")
        layout.addWidget(save_button)
        self.setLayout(layout)

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Selecionar a pasta")
        if folder:
            self.path_input.setText(folder)
    