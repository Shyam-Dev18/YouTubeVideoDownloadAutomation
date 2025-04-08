# Project Title

## Overview
This project automates the workflow of downloading videos of Highest Available Resolution, storing metadata, and optionally uploading them to Google Drive. It performs the following steps:

Downloads a video and returns its local file path.

Validates and updates spreadsheet headers as needed.

Appends metadata (title, source, date, etc.) to a Google Sheet.

If UPLOAD_TO_DRIVE is enabled, uploads the video to Google Drive and records the file ID in the sheet.

If not, stores the local file path in the sheet instead.

Includes robust error handling for each step.

Ideal for organizing and managing large batches of videos efficiently.

## Prerequisites
Before you begin, ensure you have met the following requirements:
- Python 3.x installed on your system.
- Access to Google Cloud Platform.

## Google Cloud Project Setup
1. **Create a Google Cloud Project:**
   - Go to the [Google Cloud Console](https://console.cloud.google.com/).
   - Create a new project.

2. **Enable APIs:**
   - Navigate to the "API & Services" dashboard.
   - Enable the following APIs:
     - Google Drive API
     - Google Sheets API

3. **Create Service Account:**
   - Go to "IAM & Admin" > "Service Accounts".
   - Click "Create Service Account".
   - Fill in the details and click "Create".
   - Assign the role `Editor` or `Owner` to the service account.
   - Click "Done".

4. **Generate Service Account Key:**
   - Click on the created service account.
   - Go to the "Keys" tab.
   - Click "Add Key" > "Create New Key".
   - Choose JSON format and click "Create".
   - Save the generated JSON file as `google_service_account_creds.json`.

5. **Place Credentials:**
   - Move the `google_service_account_creds.json` file to the `credentials` folder in your project directory.

6. **Share Drive Folder with Service Account**
    - Locate the Folder: Go to your Google Drive (drive.google.com) and find the folder you want to share.
    - Right-Click the Folder: Right-click on the folder.
    - Select "Share": In the context menu, click on "Share".
    - Add the Service Account Email:

    - In the "Add people and groups" field, enter the email address of your service account.
    - Set Permissions:

    - Use the dropdown menu next to the service account's email to set the permission level:
    - Editor: The service account can view, edit, delete, and add files within the folder.

    - Click "Send": Click the "Send" button to share the folder.

7. **Share Spreadsheet with service account:**
- Go to your Google Sheets (sheets.google.com) and find the spreadsheet you want to shar
- Right-Click the Spreadsheet: Right-click on the spreadsheet.
- Select "Share": In the context menu, click on "Share".
- Add the Service Account Email:
- In the "Add people and groups" field, enter the email address of your service account.
- Set Permissions:
- Use the dropdown menu next to the service account's email to set the permission level:
- Editor: The service account can view, edit, delete, and add files within the spreadsheet.
- Click "Send": Click the "Send" button to share the spreadsheet.


## FFmpeg Installation
### Option 1: Install FFmpeg on Your System
- For Windows, download the FFmpeg executable from [FFmpeg's official website](https://ffmpeg.org/download.html) and follow the installation instructions.
- For macOS, you can install FFmpeg using Homebrew:
  ```bash
  brew install ffmpeg
  ```
- For Linux, you can install FFmpeg using your package manager:
  ```bash
  sudo apt-get install ffmpeg
  ```

### Option 2: Include FFmpeg Executable in Project
- If you prefer not to install FFmpeg globally, you can download the FFmpeg executable and place it in the project directory as `ffmpeg`.

## Environment Variables
Create a `.env` file in the root of your project directory with the following content:
```env
DRIVE_ID=your_drive_id
SPREADSHEET_ID=your_spreadsheet_id
```
Replace `your_drive_id` and `your_spreadsheet_id` with the actual IDs.

## Configuration
Modify the `config.py` file to set the following options:
- `UPLOAD_TO_DRIVE`: Set to `True` or `False` to enable or disable uploading to Google Drive.
- `FFMPEG_INSTALLED`: Set to `True` if FFmpeg is installed on your system, otherwise set to `False`.

## Install Required Python Packages
Make sure you have the latest version of `yt-dlp` installed. Run the following command:
```bash
pip install --upgrade yt-dlp
```

## Additional Instructions
- Make sure you have the necessary permissions to access the Google Drive and Google Sheets APIs.
- Ensure that the service account email is added to the Google Sheets and Google Drive permissions.
- If you encounter any issues with FFmpeg, ensure that it is installed correctly and the executable is
-Read README.md Carefully.
## Project Structure

```bash 
- project-root/
 ├── credentials/google_service_account_creds.json  # Google service account credentials
 ├── ffmpeg/                       # (Optional) FFmpeg binaries for processing
 ├── storage/
 │       ├──videos               # Downloaded videos stored here.
 │       └──logs/                # Logs
 ├── utils/
 │    ├──__init__.py
 │       ├──download_videos.py  # Download Logic
 │      ├──spreadsheet.py       # Spreadsheet Logic
 │     └──upload_to_drive.py    # Upload to Google Drive Logic              
 ├── config.py
 ├── .env
 └── main.py
```

## Running the Project
```bash
python main.py
```
## 🛠️ Setup & Usage Instructions
1. **Clone the Repository**
```bash
git clone https://github.com/your-username/your-project.git
cd your-project
```
2. **Install Required Packages**
```bash
pip install -r requirements.txt
```
## Running the Project
```bash
python main.py
```

## License
This project is licensed under the MIT License.
                                                            @shyamDev18
