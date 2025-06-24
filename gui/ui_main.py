from PySide6.QtWidgets import (
    QWidget, QPushButton, QLabel, QLineEdit, QFileDialog,
    QVBoxLayout, QTabWidget, QMessageBox, QHBoxLayout, QGroupBox,
    QProgressBar, QTextEdit, QApplication, QComboBox, QStackedWidget, QSizePolicy
)
from PySide6.QtCore import QStandardPaths
from gui.styles import MINIMAL_STYLE
from .worker_audio import DownloadAudioWorker
from .worker_video import DownloadVideoWorker
from .sidebar import Sidebar, HomeScreen, SettingsScreen
#from core.instagram import download_video_instagram
from PySide6.QtGui import QIcon
from core.translations import translations
from core.config import load_config, save_config

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.config = load_config()
        self.lang = self.config.get("language", "pt")
        self.t = translations[self.lang] #referência direta à tradução
        
        self.setWindowTitle("Downloader Midia")
        self.setWindowIcon(QIcon("assets/icon.png"))
        self.resize(600, 200)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setStyleSheet(MINIMAL_STYLE)

        main_layout = QVBoxLayout()
        self.sidebar = Sidebar()
        self.sidebar.change_scr.connect(self.switch_screen)
        self.content_area = QStackedWidget()

        # A interface principal será um widget (a tela principal), definindo as interfaces
        self.main_screen = QWidget()
        self.main_screen.setLayout(self.init_ui())  # retorna o layout já montado
        self.home_screen = HomeScreen()
        self.settings_screen = SettingsScreen(self.lang)
        
        # conecta o sinal de mudança de idioma
        self.settings_screen.language_changed.connect(self.change_language)

        self.content_area.addWidget(self.main_screen)
        self.content_area.addWidget(self.home_screen)
        self.content_area.addWidget(self.settings_screen)

        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.content_area, 1)
        self.setLayout(main_layout)

    def switch_screen(self, screen_name):
        if screen_name == "home":
            self.content_area.setCurrentWidget(self.main_screen)
        elif screen_name == "settings":
            self.content_area.setCurrentWidget(self.settings_screen)
            
    def change_language(self, lang_code):
        self.config["language"] = lang_code
        save_config(self.config)
        QMessageBox.information(self, self.t["changed_language"], self.t["restart_app"])

    def init_ui(self):
        layout = QVBoxLayout()

        # Header
        header = QLabel(self.t["title"])
        header.setStyleSheet("font-size: 1.8em; font-weight: bold;")
        layout.addWidget(header)

        # Tabs
        self.tabs = QTabWidget()
        self.tabs.addTab(self.youtube_tab_ui(), "YouTube")
        #self.tabs.addTab(self.instagram_tab_ui(), "Instagram")
        layout.addWidget(self.tabs)

        # Progresso e Logs
        self.progress = QProgressBar()
        self.logs = QTextEdit()
        self.logs.setReadOnly(True)
        self.logs.setPlaceholderText(self.t["logs_placeholder"])
        layout.addWidget(self.progress)
        layout.addWidget(self.logs)

        # Rodapé
        footer = QLabel(self.t["footer"])
        footer.setStyleSheet("font-size: 0.8em; color: #888;")
        layout.addWidget(footer)

        return layout

    def youtube_tab_ui(self):
        widget = QWidget()
        layout = QVBoxLayout()

        url_group = QGroupBox(self.t["url_input"])
        url_layout = QHBoxLayout()
        self.youtube_url = QLineEdit()
        self.youtube_url.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        url_layout.addWidget(self.youtube_url)
        url_group.setLayout(url_layout)
        layout.addWidget(url_group)

        output_group = QGroupBox(self.t["save"])
        output_layout = QHBoxLayout()
        self.output_dir = QLineEdit()
        self.output_dir.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        browse_button = QPushButton(self.t["folder"])

        filename_group = QGroupBox(self.t["archive_name"])
        filename_layout = QHBoxLayout()
        self.filename_input = QLineEdit()
        self.filename_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.filename_input.setText("download_midia")
        filename_layout.addWidget(self.filename_input)
        #ext_label = QLabel(".mp3")
        #filename_layout.addWidget(ext_label)
        filename_group.setLayout(filename_layout)
        layout.addWidget(filename_group)

        desktop_path = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DesktopLocation)
        self.output_dir.setText(desktop_path)
        browse_button.clicked.connect(self.select_output_dir)
        output_layout.addWidget(self.output_dir)
        output_layout.addWidget(browse_button)
        output_group.setLayout(output_layout)
        layout.addWidget(output_group)

        # Parte do Vídeo
        actions_layout_video = QVBoxLayout()
        video_group = QGroupBox(self.t["video_download"])
        video_layout = QVBoxLayout()
        self.quality_selector = QComboBox()
        self.quality_selector.addItems([
            self.t["best"],
            "1080p",
            "720p",
            "480p"
        ])
        video_layout.addWidget(QLabel(self.t["quality"]))
        video_layout.addWidget(self.quality_selector)
        convert_button_video = QPushButton(self.t["download_video"])
        convert_button_video.clicked.connect(self.download_youtube_video)
        video_layout.addWidget(convert_button_video)

        video_group.setLayout(video_layout)
        actions_layout_video.addWidget(video_group)
        video_group.setLayout(actions_layout_video)
        layout.addWidget(video_group)
        
        # Parte do Áudio
        actions_group_audio = QGroupBox()
        actions_layout_audio = QVBoxLayout()
        audio_group = QGroupBox(self.t["audio_download"])
        audio_layout = QVBoxLayout()
        convert_button_audio = QPushButton(self.t["download_audio"])
        convert_button_audio.clicked.connect(self.download_youtube_audio)
        audio_layout.addWidget(convert_button_audio)

        audio_group.setLayout(audio_layout)
        actions_layout_audio.addWidget(audio_group)
        actions_group_audio.setLayout(actions_layout_audio)
        layout.addWidget(actions_group_audio)

        widget.setLayout(layout)
        return widget

    '''def instagram_tab_ui(self):
        widget = QWidget()
        layout = QVBoxLayout()

        url_group = QGroupBox("Cole sua URL aqui:")
        url_layout = QHBoxLayout()
        self.instagram_url = QLineEdit()
        url_layout.addWidget(self.instagram_url)
        url_group.setLayout(url_layout)
        layout.addWidget(url_group)

        output_group = QGroupBox("Salvar em:")
        output_layout = QHBoxLayout()
        self.output_dir_ig = QLineEdit()
        browse_button = QPushButton("Procurar")
        browse_button.clicked.connect(self.select_output_dir_ig)
        output_layout.addWidget(self.output_dir_ig)
        output_layout.addWidget(browse_button)
        output_group.setLayout(output_layout)
        layout.addWidget(output_group)

        actions_group = QGroupBox("Ação")
        actions_layout = QHBoxLayout()
        download_button = QPushButton("Baixar Vídeo IG")
        download_button.clicked.connect(self.download_video_instagram_ui)
        actions_layout.addWidget(download_button)
        actions_group.setLayout(actions_layout)
        layout.addWidget(actions_group)

        widget.setLayout(layout)
        return widget'''
    
    def select_output_dir(self):
        path = QFileDialog.getExistingDirectory(self, self.t["folder_directory"])
        if path:
            self.output_dir.setText(path)

    '''def select_output_dir_ig(self):
        path = QFileDialog.getExistingDirectory(self, "Selecionar Diretório")
        if path:
            self.output_dir_ig.setText(path)'''

    def show_message(self, message):
        QMessageBox.information(self, "Info", message)

    def log(self, message):
        self.logs.append(message)
        QApplication.processEvents()  # força atualização da UI para mostrar o texto imediatamente

    def download_youtube_audio(self):
        url = self.youtube_url.text().strip()
        output = self.output_dir.text().strip()
        filename = self.filename_input.text().strip() or "audio"

        if not url or not output:
            self.show_message(self.t["status_message"])
            return

        self.logs.clear()

        self.worker = DownloadAudioWorker(url, output, filename)
        self.worker.log_signal.connect(self.log)
        self.worker.finished_signal.connect(self.on_process_finished)
        self.worker.error_signal.connect(self.on_process_error)
        self.worker.start()
        
    def download_youtube_video(self):
        url = self.youtube_url.text().strip()
        output = self.output_dir.text().strip()
        filename = self.filename_input.text().strip() or "video"
        quality = self.quality_selector.currentText()

        if not url or not output:
            self.show_message(self.t["status_message"])
            return

        self.logs.clear()

        self.worker = DownloadVideoWorker(url, output, filename, quality)
        self.worker.log_signal.connect(self.log)
        self.worker.finished_signal.connect(self.on_process_finished)
        self.worker.error_signal.connect(self.on_process_error)
        self.worker.start()
    
    def log(self, message):
        self.logs.append(message)
        QApplication.processEvents()

    def on_process_finished(self, transcription_path):
        self.log(f"O áudio está salvo em: {transcription_path}")
        self.show_message(self.t["sucess_download"])

    def on_process_error(self, error_msg):
        self.log(f"Erro: {error_msg}")
        self.show_message(self.t["error_download"], {error_msg})

    '''def download_video_instagram_ui(self):
        url = self.instagram_url.text()
        output = self.output_dir_ig.text()
        if url and output:
            try:
                download_video_instagram(url, output)
                self.show_message("Download do vídeo IG concluído!")
            except Exception as e:
                self.show_message(f"Erro: {str(e)}")'''
