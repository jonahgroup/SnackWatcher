#!/bin/sh
# Build the Docker images from scratch
echo [BUILD]
sh docker_stop.sh | sed "s/^/\t/"
if [ ! -d "SnackWatcher" ]; then
    echo [Clone a new copy of SnackWatcher]
    git clone --depth 1 https://github.com/jonahgroup/SnackWatcher.git
fi
echo [Build snack-db]
docker build -t snackwatcher/snack-db SnackWatcher/scripts/mongodb
echo [Build snack-web]
docker build -t snackwatcher/snack-web SnackWatcher
