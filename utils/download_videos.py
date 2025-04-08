import yt_dlp
import os
import logging
from config import Settings

def download_youtube_video(url: str, settings: Settings) -> str | None:
    filename = "%(title).100s.%(ext)s"  # Limit filename length
    try:
        logging.info(f"Starting download for URL: {url}")
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': os.path.join(settings.VIDEO_DIR, filename),
            'merge_output_format': 'mp4',
            'nopart': True,
            'retries': settings.MAX_RETIES,
            'fragment_retries': settings.MAX_RETIES,
            'quiet': False,
            'no_warnings': True,
            'restrict-filenames': True,
            'postprocessors': [
                {'key': 'FFmpegVideoRemuxer', 'preferedformat': 'mp4'},
            ]
        }

        if not settings.FFMPEG_INSTALLED_IN_SYSTEM:
            print("\n✅ FFmpeg not installed in system. Using local FFmpeg.\n")
            logging.info("FFmpeg not installed in system. Using local FFmpeg.")
            ydl_opts['ffmpeg_location'] = settings.FFMPEG

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.download([url])
            if result == 0:
                logging.info("Download completed successfully.")
                return ydl.prepare_filename(ydl.extract_info(url, download=False))
            else:
                logging.error("Download failed.")
                return None
    except Exception as e:
        logging.error(f"Error downloading video: {str(e)}", exc_info=True)
        return None