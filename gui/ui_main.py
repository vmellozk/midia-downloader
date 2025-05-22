from PySide6.QtWidgets import (
    QWidget, QPushButton, QLabel, QLineEdit, QFileDialog,
    QVBoxLayout, QTabWidget, QMessageBox, QHBoxLayout, QGroupBox,
    QProgressBar, QTextEdit, QApplication, QComboBox
)
from PySide6.QtCore import QStandardPaths
from gui.styles import MINIMAL_STYLE
from .worker_audio import DownloadAudioWorker
from .worker_video import DownloadVideoWorker

from core.instagram import download_video_instagram
from PySide6.QtGui import QIcon

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Downloader Midia")
        self.setWindowIcon(QIcon("assets/icon.png"))
        self.setMinimumSize(600, 400)
        self.setStyleSheet(MINIMAL_STYLE)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Header
        header = QLabel("⬇️ Baixar Áudio e Vídeo")
        header.setStyleSheet("font-size: 20pt; font-weight: bold;")
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
        self.logs.setPlaceholderText("Log de atividades...")
        layout.addWidget(self.progress)
        layout.addWidget(self.logs)

        # Rodapé
        footer = QLabel("Criado com 💙 por vmellozk")
        footer.setStyleSheet("font-size: 10pt; color: #888;")
        layout.addWidget(footer)

        self.setLayout(layout)

    def youtube_tab_ui(self):
        widget = QWidget()
        layout = QVBoxLayout()

        url_group = QGroupBox("Cole sua URL aqui:")
        url_layout = QHBoxLayout()
        self.youtube_url = QLineEdit()
        url_layout.addWidget(self.youtube_url)
        url_group.setLayout(url_layout)
        layout.addWidget(url_group)

        output_group = QGroupBox("Salvar em:")
        output_layout = QHBoxLayout()
        self.output_dir = QLineEdit()
        browse_button = QPushButton("Pasta de destino")
        
        filename_group = QGroupBox("Nome do arquivo:")
        filename_layout = QHBoxLayout()
        self.filename_input = QLineEdit()
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

        actions_group = QGroupBox("Ação")
        actions_layout = QVBoxLayout()
        
        # ComboBox de Qualidade
        self.quality_selector = QComboBox()
        self.quality_selector.addItems([
            "Melhor (Automático)",
            "1080p",
            "720p",
            "480p",
            "Áudio apenas"
        ])
        actions_layout.addWidget(QLabel("Qualidade do vídeo:"))
        actions_layout.addWidget(self.quality_selector)

        # Botões de ação
        button_layout = QHBoxLayout()
        convert_button_audio = QPushButton("Baixar Áudio")
        convert_button_audio.clicked.connect(self.download_youtube_audio)
        convert_button_video = QPushButton("Baixar Vídeo")
        convert_button_video.clicked.connect(self.download_youtube_video)

        button_layout.addWidget(convert_button_audio)
        button_layout.addWidget(convert_button_video)

        actions_layout.addLayout(button_layout)
        actions_group.setLayout(actions_layout)
        layout.addWidget(actions_group)

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
        path = QFileDialog.getExistingDirectory(self, "Selecionar Diretório")
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
            self.show_message("Por favor, preencha a URL e o diretório de saída.")
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
            self.show_message("Por favor, preencha a URL e o diretório de saída.")
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
        self.show_message("Download realizado com sucesso!")

    def on_process_error(self, error_msg):
        self.log(f"Erro: {error_msg}")
        self.show_message(f"Ocorreu um erro: {error_msg}")

    def download_video_instagram_ui(self):
        url = self.instagram_url.text()
        output = self.output_dir_ig.text()
        if url and output:
            try:
                download_video_instagram(url, output)
                self.show_message("Download do vídeo IG concluído!")
            except Exception as e:
                self.show_message(f"Erro: {str(e)}")
 