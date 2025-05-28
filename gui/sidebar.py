from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QPushButton, QLabel,
    QVBoxLayout, QComboBox, QCheckBox, QLineEdit,
    QFileDialog
)
from PySide6.QtCore import Signal, Qt
from core.translations import translations
from core.config import save_config, load_config

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
    language_changed = Signal(str)
    
    def __init__(self, current_lang):
        super().__init__()
        self.config = load_config()
        self.lang = self.config.get("language", "pt")
        self.t = translations[self.lang]  # Referência à tradução
        
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # Título
        title = QLabel(self.t["config_app"])
        title.setStyleSheet("font-size: 18pt; font-weight: bold;")
        layout.addWidget(title)
        
        # Seção: Idioma
        layout.addWidget(QLabel(self.t["language"]))
        self.language_combo = QComboBox()
        self.language_combo.addItems(["Português (PT-BR)", "English (EN)", "Español"])
        self.language_combo.setCurrentText(self.lang_display(current_lang))
        layout.addWidget(self.language_combo)
        
        # Seção: Tema
        layout.addWidget(QLabel(self.t["theme"]))
        self.theme_checkbox = QCheckBox(self.t["dark_mode"])
        layout.addWidget(self.theme_checkbox)
        
        # Seção: Caminho Padrão de Download
        layout.addWidget(QLabel(self.t["download_folder"]))
        path_layout = QHBoxLayout()
        self.path_input = QLineEdit()
        self.path_button = QPushButton(self.t["select_folder"])
        self.path_button.clicked.connect(self.select_folder)
        path_layout.addWidget(self.path_input)
        path_layout.addWidget(self.path_button)
        layout.addLayout(path_layout)
        
        # Seção: Preferências
        self.auto_open_checkbox = QCheckBox(self.t["open_folder"])
        layout.addWidget(self.auto_open_checkbox)
        
        # Botão de Salvar
        save_button = QPushButton(self.t["save_button"])
        save_button.clicked.connect(self.save_settings)
        layout.addWidget(save_button)
        
        self.setLayout(layout)

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, self.t["select_folder"])
        if folder:
            self.path_input.setText(folder)
            
    def lang_display(self, lang_code):
        if lang_code == "pt":
            return "Português (PT-BR)"
        elif lang_code == "en":
            return "English (EN)"
        elif lang_code == "es":
            return "Español"
        return "Português (PT-BR)"  # fallback
    
    def save_settings(self):
        lang_text = self.language_combo.currentText()
        if "Português" in lang_text:
            lang_code = "pt"
        elif "English" in lang_text:
            lang_code = "en"
        elif "Español" in lang_text:
            lang_code = "es"
        else:
            lang_code = "pt"  # fallback caso inesperado
        
        save_config({"language": lang_code})
        self.language_changed.emit(lang_code)
