from PySide6.QtCore import QThread, Signal
import os
import time
from core.youtube import download_audio_youtube
from core.translations import translations
from core.config import load_config

class DownloadAudioWorker(QThread):
    log_signal = Signal(str)
    finished_signal = Signal(str)
    error_signal = Signal(str)

    def __init__(self, url, output_dir, filename):
        super().__init__()
        self.config = load_config()
        self.lang = self.config.get("language", "pt")
        self.t = translations[self.lang] #referência direta à tradução
        
        self.url = url
        self.output_dir = output_dir
        self.filename = filename
        
    def log(self, message):
        self.log_signal.emit(message)

    def run(self):
        try:
            self.log(self.t["process_audio"])
            time.sleep(3)

            audio_base = os.path.join(self.output_dir, self.filename)
            counter = 1
            while os.path.exists(f"{audio_base}.mp3"):
                audio_base = f"{os.path.join(self.output_dir, self.filename)}_{counter}"
                counter += 1
            audio_path = f"{audio_base}.mp3"

            self.log(self.t["download_and_convert_audio"])
            download_audio_youtube(self.url, audio_base)

            self.log(self.t["finishing_download"])
            audio_path = f"{audio_base}.mp3"

            self.finished_signal.emit(audio_path)

        except Exception as e:
            self.error_signal.emit(str(e))
