import os
import time
import shutil
import ftplib
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import xml.etree.ElementTree as ET
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# FTP Configuration
FTP_HOST = os.getenv("FTP_HOST")
FTP_USER = os.getenv("FTP_USER")
FTP_PASS = os.getenv("FTP_PASS")

# Folder Paths
TEMP_FOLDER = './temp'
LOCAL_FOLDER = './local'
TRASH_FOLDER = './trash'

# Ensure directories exist
os.makedirs(TEMP_FOLDER, exist_ok=True)
os.makedirs(LOCAL_FOLDER, exist_ok=True)
os.makedirs(TRASH_FOLDER, exist_ok=True)


class FileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        file_path = event.src_path
        if file_path.endswith('.xml'):
            process_file(file_path)


def process_file(file_path):
    try:
        # Parse the XML file
        tree = ET.parse(file_path)
        root = tree.getroot()

        # Extract values into a dictionary
        data = {}
        for child in root:
            data[child.tag] = child.text

        # Print the dictionary
        print(data)

        # Move the file to the trash folder
        shutil.move(file_path, os.path.join(TRASH_FOLDER, os.path.basename(file_path)))
    except Exception as e:
        print(f"Failed to process file {file_path}: {e}")


def download_files():
    try:
        with ftplib.FTP(FTP_HOST, FTP_USER, FTP_PASS) as ftp:
            ftp.cwd('/')
            filenames = ftp.nlst()
            for filename in filenames:
                if filename.endswith('.xml'):
                    local_temp_path = os.path.join(TEMP_FOLDER, filename)
                    with open(local_temp_path, 'wb') as f:
                        ftp.retrbinary(f'RETR {filename}', f.write)
                    shutil.move(local_temp_path, os.path.join(LOCAL_FOLDER, filename))
    except Exception as e:
        print(f"Failed to download files: {e}")


if __name__ == "__main__":
    observer = Observer()
    event_handler = FileHandler()
    observer.schedule(event_handler, path=LOCAL_FOLDER, recursive=False)
    observer.start()

    try:
        while True:
            download_files()
            time.sleep(10)  # Check for new files every 10 seconds
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
