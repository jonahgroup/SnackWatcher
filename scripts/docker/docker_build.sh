#!/bin/sh
# Build the Docker images from scratch
echo [BUILD]
sh snack_init.sh | sed "s/^/\t/"
echo [Build snack-db]
docker build -t snackwatcher/snack-db SnackWatcher/scripts/mongodb
echo [Build snack-web]
docker build -t snackwatcher/snack-web SnackWatcher
