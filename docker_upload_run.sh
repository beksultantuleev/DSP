#!/bin/bash

# Navigate to the directory where the script and docker-compose.yml live
cd "$(dirname "$0")"

echo "Starting DSP Upload via Docker Compose..."

# --build ensures it picks up any new code changes you make
# --abort-on-container-exit stops the compose network as soon as the python script finishes
# --rm removes the stopped container afterward to keep the client's system clean
docker compose up --build --abort-on-container-exit
docker compose rm -f

echo "Container execution finished."