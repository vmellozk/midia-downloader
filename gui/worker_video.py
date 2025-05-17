from PySide6.QtCore import QThread, Signal
import os
import time
from core.youtube import download_video_youtube

class DownloadVideoWorker(QThread):
    log_signal = Signal(str)
    finished_signal = Signal(str)
    error_signal = Signal(str)

    def __init__(self, url, output_dir, filename):
        super().__init__()
        self.url = url
        self.output_dir = output_dir
        self.filename = filename
        
    def log(self, message):
        self.log_signal.emit(message)

    def run(self):
        try:
            self.log("Processando o vídeo para começar o download...")
            time.sleep(3)

            video_base = os.path.join(self.output_dir, self.filename)
            counter = 1
            while os.path.exists(f"{video_base}.mp4"):
                video_base = f"{os.path.join(self.output_dir, self.filename)}_{counter}"
                counter += 1
            video_path = f"{video_base}.mp4"

            self.log("Baixando e convertendo o vídeo para mp4...")
            download_video_youtube(self.url, video_base)

            self.log("Finalizando o download e salvando o arquivo...")
            self.finished_signal.emit(video_path)

        except Exception as e:
            self.error_signal.emit(str(e))
