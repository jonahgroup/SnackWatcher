#!/bin/sh
# Build the Docker images from scratch
echo [BUILD]
sh snack_stop.sh | sed "s/^/\t/"
echo [Build snack-db]
docker build -t snackwatcher/snack-db snack-db
echo [Build snack-web]
docker build -t snackwatcher/snack-web snack-web
