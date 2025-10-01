#!/bin/bash
# Script to run Stock Notifier in Docker

# Change to the script's directory
cd "$(dirname "$0")"

# Build the image (optional - remove if image is already built)
# docker build -t stock-notifier .

# Run the container
docker run --rm stock-notifier

# Exit with the same status as the docker command
exit $?

