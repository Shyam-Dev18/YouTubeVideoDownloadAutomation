import os
import logging
from datetime import datetime
from config import Settings
from utils.download_videos import download_youtube_video
from utils.spreadsheet import update_spreadsheet

def configure_logging(settings):
    """Configure logging to create a new log file daily and log to console."""
    os.makedirs(settings.LOG_DIR, exist_ok=True)
    log_file = f"{settings.LOG_DIR}/{datetime.now().strftime('%d-%m-%Y')}.log"

    # Create a logger
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO))

    # File handler
    file_handler = logging.FileHandler(log_file, encoding="utf-8")  # Ensure UTF-8 encoding for the log file
    file_handler.setFormatter(logging.Formatter(settings.LOG_FORMAT))
    logger.addHandler(file_handler)

    # Console handler
    #console_handler = logging.StreamHandler()
    #console_handler.setFormatter(logging.Formatter(settings.LOG_FORMAT))
    #console_handler.stream = open(console_handler.stream.fileno(), mode='w', encoding='utf-8', buffering=1)  # Force UTF-8 encoding
    #logger.addHandler(console_handler)

    return logger

def main():
    settings = Settings()
    logging = configure_logging(settings)

    logging.info("Application started.")

    while True:
        try:
            video_url = input("\nEnter YouTube URL (q to quit): ").strip()
            
            if video_url.lower() == 'q':
                logging.info("User exited the application.\n\n")
                print("\nExiting...")
                break
                
            if not video_url:
                logging.warning("Empty URL entered.")
                print("URL cannot be empty!")
                continue
            
            logging.info(f"Processing video: {video_url}")
            print("\nProcessing video... Please wait.\n")

            file_path = download_youtube_video(video_url, settings)
            if file_path:
                logging.info(f"Video downloaded successfully: {file_path}")
                update_spreadsheet(video_url, file_path, settings)
            else:
                logging.error("Download failed. Metadata update skipped.")
                print("❌ Download failed. Metadata update skipped.")
            
        except KeyboardInterrupt:
            logging.warning("Operation cancelled by user.")
            print("\n\nOperation cancelled by user.")
            break
            
        except Exception as e:
            logging.error(f"Unexpected error: {str(e)}", exc_info=True)
            print(f"\nUnexpected error: {str(e)}")

if __name__ == "__main__":
    main()