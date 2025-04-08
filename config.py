"""
Application settings and configuration management.
Uses environment variables and .env file for configuration.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(encoding='utf-8')

class Settings:
    def __init__(self):
        self.BASE_DIR = Path(__file__).parent
        self.STORAGE_DIR = self.BASE_DIR / "storage"
        self.VIDEO_DIR = self.STORAGE_DIR / "videos"
        self.LOG_DIR = self.STORAGE_DIR / "logs"
        self.CREDENTIALS_DIR = self.BASE_DIR / "credentials"

        self.FFMPEG_INSTALLED_IN_SYSTEM = True
        self.FFMPEG = self.BASE_DIR / "ffmpeg" / "bin"


        self.GOOGLE_CREDS_PATH = self.CREDENTIALS_DIR / "google_service_account_creds.json"
        self.SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
        self.DRIVE_FOLDER_ID = os.getenv("DRIVE_FOLDER_ID")
        self.SHEET_NAME = "Sheet1"

        self.METADATA_HEADERS = [
            "Title", "Description", "Tags", "Category", "Drive File ID/Local_storage",
            "Playlist", "Thumbnail", "Upload Date", "Download Status", "Upload Status"
        ]

        self.PLAYLIST = "Testing"
        self.MAX_RETIES = 3
        self.RETRY_DELAY = 5

        #Drive upload settings
        self.CHUNK_SIZE = 50 * 1024 * 1024 # 50 MB
        self.UPLOAD_TO_DRIVE = False

        ## Logging settings
        self.LOG_LEVEL =  "INFO"
        self.LOG_FORMAT = "%(asctime)s - %(levelname)s - [%(name)s] - %(message)s"

        if not self.SPREADSHEET_ID:
            raise ValueError("SPREADSHEET_ID environment variable is required")
        if not self.DRIVE_FOLDER_ID:
            raise ValueError("DRIVE_FOLDER_ID environment variable is required")