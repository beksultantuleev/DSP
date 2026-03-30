from upload_csv_to_DSP import *
import os
import shutil
from datetime import datetime

# Read from environment, default to the container's designated mount path
SORTED_DF_CSV_PATH = os.getenv("CSV_FILE_PATH", "/app/raw_data/subs_info_data.csv")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC")

# Define where finished files go (this will be created inside the mapped local folder)
ARCHIVE_DIR = "/app/raw_data/archive"

# 1. Check if there is even a file to process
if not os.path.exists(SORTED_DF_CSV_PATH):
    print(f"No new data found at {SORTED_DF_CSV_PATH}. Exiting cleanly.")
    exit(0)

# 2. Ensure the archive directory exists
os.makedirs(ARCHIVE_DIR, exist_ok=True)

# 3. Attempt the upload
try:
    print(f"Starting upload for {SORTED_DF_CSV_PATH}...")
    upload_via_api_gateway(SORTED_DF_CSV_PATH, KAFKA_TOPIC)
    
    # 4. If successful, rename and move the file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    original_filename = os.path.basename(SORTED_DF_CSV_PATH)
    archived_filename = f"{timestamp}_{original_filename}"
    
    archive_path = os.path.join(ARCHIVE_DIR, archived_filename)
    
    shutil.move(SORTED_DF_CSV_PATH, archive_path)
    print(f"Success! File moved to {archive_path}")

except Exception as e:
    # If the upload fails, we do NOT move the file. 
    # It stays exactly where it is so the next cron run can try again.
    print(f"Upload failed: {e}")
    exit(1)