import yt_dlp
import sys
import os
import subprocess
import glob
import platform

def resource_path(relative_path):
    # Para suportar PyInstaller
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def get_ffmpeg_path():
    if platform.system() == "Windows":
        ffmpeg_dir = resource_path(os.path.join("ffmpeg", "bin"))
        ffmpeg_exec = os.path.join(ffmpeg_dir, "ffmpeg.exe")
    else:
        ffmpeg_dir = "/usr/bin"
        ffmpeg_exec = "ffmpeg"  # já está no PATH
    return ffmpeg_dir, ffmpeg_exec

def download_audio_youtube(video_url, output_path):
    try:
        ffmpeg_dir, _ = get_ffmpeg_path()  # usa-se ffmpeg_dir de acordo

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': output_path,
            'ffmpeg_location': ffmpeg_dir,  # <- diretório, não executável!
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
    except Exception as e:
        print("Erro no download do áudio:", str(e))

def download_video_youtube(video_url, output_path, quality):
    try:
        ffmpeg_dir, ffmpeg_exec = get_ffmpeg_path()
        base_path = os.path.splitext(output_path)[0]
        final_output = base_path + ".mp4"
        
        #pasta cache
        cache_dir = os.path.join(os.path.abspath("."), "cache")
        os.makedirs(cache_dir, exist_ok=True)

        downloaded_files = []

        def hook(d):
            if d['status'] == 'finished':
                downloaded_files.append(d['filename'])

        # Mapeamento da qualidade para os formatos yt-dlp
        quality_map = {
            "Melhor (Automático)": "bestvideo[ext=mp4]+bestaudio[ext=webm]/best",
            "1080p": "137+bestaudio/best[height<=1080]",
            "720p": "22/best[height<=720]",
            "480p": "135+bestaudio/best[height<=480]"
        }

        selected_format = quality_map.get(quality, "bestvideo[ext=mp4]+bestaudio[ext=webm]/best")

        ydl_opts = {
            'format': selected_format,
            'outtmpl': os.path.join(cache_dir, 'temp_video.%(format_id)s.%(ext)s'),
            'ffmpeg_location': ffmpeg_dir,  # <- aqui também usa o diretório
            'noplaylist': True,
            'progress_hooks': [hook],
            'keepvideo': True,  # <-- ESSENCIAL PARA EVITAR A DELEÇÃO DOS ARQUIVOS
            'merge_output_format': None,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        # Identifica os arquivos baixados
        video_file = next((f for f in downloaded_files if f.endswith(".mp4")), None)
        audio_file = next((f for f in downloaded_files if f.endswith(".webm")), None)

        if not video_file or not audio_file:
            raise Exception("Não foi possível localizar os arquivos baixados.")

        # Merge com ffmpeg
        cmd = [
            ffmpeg_exec,
            '-i', video_file,
            '-i', audio_file,
            '-c:v', 'copy',
            '-c:a', 'aac',
            '-strict', 'experimental',
            '-y',
            final_output
        ]
        subprocess.run(cmd, check=True)

        # Remove temporários
        os.remove(video_file)
        os.remove(audio_file)
        
        # Apaga arquivos extra gerados no cache
        extra_files = glob.glob(os.path.join(cache_dir, "temp_video.*+*.webm"))
        for f in extra_files:
            os.remove(f)

        print(f"✅ Vídeo salvo em: {final_output}")

    except Exception as e:
        print("Erro no download do vídeo:", str(e))
