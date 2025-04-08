import os
import logging
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError
from config import Settings

def upload_to_drive(file_path: str, settings: Settings) -> str | None:
    try:
        logging.info(f"Uploading file to Google Drive: {file_path}")
        print("\n📤 Uploading to Google Drive...")
        
        creds = Credentials.from_service_account_file(
            settings.GOOGLE_CREDS_PATH,
            scopes=["https://www.googleapis.com/auth/drive"]
        )
        drive_service = build("drive", "v3", credentials=creds)

        file_metadata = {
            "name": os.path.basename(file_path),
            "mimeType": "video/mp4",
        }
        if settings.DRIVE_FOLDER_ID:
            file_metadata["parents"] = [settings.DRIVE_FOLDER_ID]

        media = MediaFileUpload(file_path, mimetype="video/mp4", resumable=True, chunksize=settings.CHUNK_SIZE)
        request = drive_service.files().create(body=file_metadata, media_body=media, fields="id")

        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                progress = int(status.resumable_progress / os.path.getsize(file_path) * 100)
                print(f"\r⬆️ Uploading: {progress}% complete", end='', flush=True)

        logging.info("File uploaded successfully.")
        print(f"\n✅ File uploaded. Drive ID: {response.get('id')}")
        return response.get("id")
    except Exception as e:
        logging.error(f"Error uploading file to Google Drive: {str(e)}", exc_info=True)
        return None