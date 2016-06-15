#!/bin/sh
# Clear out the generated images and reset the database
echo [RESET]
echo [Stop any running containers]
sh snack_stop.sh | sed "s/^/\t/"
echo [Remove volumes]
sudo rm -rf ~/snack-db/data
sudo rm -rf ~/snack-web/logs
docker volume rm snack-web-images
