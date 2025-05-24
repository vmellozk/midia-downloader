from PySide6.QtCore import QThread, Signal
import os
import time
from core.youtube import download_video_youtube
from core.translations import translations
from core.config import load_config

class DownloadVideoWorker(QThread):
    log_signal = Signal(str)
    finished_signal = Signal(str)
    error_signal = Signal(str)

    def __init__(self, url, output_dir, filename, quality):
        super().__init__()
        self.config = load_config()
        self.lang = self.config.get("language", "pt")
        self.t = translations[self.lang] # referência à tradução
        
        self.url = url
        self.output_dir = output_dir
        self.filename = filename
        self.quality = quality
        
    def log(self, message):
        self.log_signal.emit(message)

    def run(self):
        try:
            self.log(self.t["process_video"])
            time.sleep(3)

            video_base = os.path.join(self.output_dir, self.filename)
            counter = 1
            while os.path.exists(f"{video_base}.mp4"):
                video_base = f"{os.path.join(self.output_dir, self.filename)}_{counter}"
                counter += 1
            video_path = f"{video_base}.mp4"

            self.log(self.t["download_and_convert_video"])
            download_video_youtube(self.url, video_base, self.quality)

            self.log(self.t["finishing_download"])
            self.finished_signal.emit(video_path)

        except Exception as e:
            self.error_signal.emit(str(e))
