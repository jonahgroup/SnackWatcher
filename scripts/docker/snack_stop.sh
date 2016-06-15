#!/bin/sh
# Stop and remove all of the running SnackWatcher containers
echo [STOP]
echo [Remove running containers]
docker ps -aq -f ancester=snack-db | xargs -r -I % docker rm -f %
docker ps -aq -f ancester=snack-web | xargs -r -I % docker rm -f %
