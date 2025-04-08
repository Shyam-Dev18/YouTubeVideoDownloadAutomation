import gspread
import datetime
from config import Settings
from utils.upload_to_drive import upload_to_drive
from google.oauth2.service_account import Credentials
from google.auth.exceptions import GoogleAuthError
import yt_dlp
import logging

def authenticate_service_account(settings: Settings):
    try:
        creds = Credentials.from_service_account_file(
            settings.GOOGLE_CREDS_PATH,
            scopes=["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        )
        return gspread.authorize(creds)
    except Exception as e:
        print(f"❌ Auth error: {e}")
        exit(1)

def validate_and_update_headers(sheet, settings: Settings):
    existing_headers = sheet.row_values(1)
    if existing_headers != settings.METADATA_HEADERS:
        print("\n⚠️ Headers mismatch. Resetting...\n")
        sheet.clear()
        sheet.append_row(settings.METADATA_HEADERS)
    else:
        print("\n✅ Spreadsheet headers are valid.")

def extract_video_metadata(url: str, settings: Settings) -> dict:
    try:
        with yt_dlp.YoutubeDL({'quiet': True, 'no_warnings': True, 'skip_download': True}) as ydl:
            info = ydl.extract_info(url, download=False)

        return {
            "Title": info.get("title", "Unknown"),
            "Description": info.get("description", "Description not available"),
            "Tags": ', '.join(info.get("tags", ['anime','manga','trending','popular'])),
            "Category": info.get('categories', ['Anime'])[0],
            "Drive File ID/Local_storage": "ERROR",  # Placeholder
            "Playlist": settings.PLAYLIST,
            "Thumbnail": info.get("thumbnail", "NO THUMBNAIL"),
            "Upload Date": datetime.datetime.now().strftime("%Y-%m-%d"),
            "Download Status": "Pending",
            "Upload Status": "Pending"
        }
    except Exception as e:
        print(f"\n❌ Metadata extraction failed: {e}\n")
        return {}

def update_spreadsheet(url: str, file_path: str, settings: Settings):
    try:
        logging.info("Updating spreadsheet with video metadata.")
        client = authenticate_service_account(settings)
        sheet = client.open_by_key(settings.SPREADSHEET_ID).worksheet(settings.SHEET_NAME)
        validate_and_update_headers(sheet, settings)

        print("\n📋 Updating spreadsheet...")
        metadata = extract_video_metadata(url, settings)

        if not metadata:
            logging.warning("No metadata extracted. Skipping spreadsheet update.")
            return

        if settings.UPLOAD_TO_DRIVE:
            file_id = upload_to_drive(file_path, settings)
            metadata["Drive File ID/Local_storage"] = file_id if file_id else "Upload failed"
            metadata["Download Status"] = "Completed" if file_id else "Failed"
        else:
            metadata["Drive File ID/Local_storage"] = file_path
            metadata["Download Status"] = "Skipped"

        sheet.append_row([metadata.get(header, "") for header in settings.METADATA_HEADERS])
        logging.info("Metadata row appended successfully.")
        print("📋 Metadata row appended.\n")
    except Exception as e:
        logging.error(f"Error updating spreadsheet: {str(e)}", exc_info=True)