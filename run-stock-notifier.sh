#!/bin/bash
# Script to run Stock Notifier in Docker

# Change to the script's directory
cd "$(dirname "$0")"

# Check if the Docker image exists, build if it doesn't
if ! docker image inspect stock-notifier >/dev/null 2>&1; then
    echo "Docker image 'stock-notifier' not found. Building..."
    docker build -t stock-notifier .
    if [ $? -ne 0 ]; then
        echo "Failed to build Docker image"
        exit 1
    fi
else
    echo "Docker image 'stock-notifier' found"
fi

# Run the container
docker run --rm stock-notifier

# Exit with the same status as the docker command
exit $?

