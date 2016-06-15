#!/bin/sh
# Build the Docker images from scratch
echo [INSTALL]
sh snack_stop.sh | sed "s/^/\t/"
echo [Pull snack-db]
docker pull snackwatcher/snack-db
echo [Pull snack-web]
docker pull snackwatcher/snack-web
