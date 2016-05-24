#!/bin/sh
# Clear out the generated images and reset the database
echo [RESET]
echo [Stop any running containers]
sh docker_stop.sh | sed "s/^/\t/"
echo [Remove volumes]
sudo rm -rf ~/snack
docker volume rm snack-web
