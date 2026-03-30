#!/bin/bash

# Always use the script's directory as working dir
cd "$(dirname "$0")" || exit 1

# Ensure logs directory exists
mkdir -p logs

# Set Oracle Instant Client path
export LD_LIBRARY_PATH=/opt/oracle/instantclient:$LD_LIBRARY_PATH

# Optional: load environment variables from .env if it exists
if [ -f ".env" ]; then
  export $(grep -v '^#' .env | xargs)
fi

# Activate virtual environment if it exists
if [ -d "virt_env" ]; then
  source virt_env/bin/activate
else
  echo "⚠️ Virtual environment not found. Skipping activation." > logs/data_upload.log
fi


# Overwrite log file at the beginning of the script
echo "▶️ Running Incremental cdp stat upload at $(date)" > logs/data_upload.log

# Run the script, overwriting output in the log file
python src/upload_csv_to_DSP.py >> logs/data_upload.log 2>&1

# Log finish
echo "✅ Finished at $(date)" >> logs/data_upload.log