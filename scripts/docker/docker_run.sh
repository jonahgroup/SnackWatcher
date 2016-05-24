#!/bin/sh
# Launch the Docker containers from the images
echo [RUN]
sh docker_stop.sh | sed "s/^/\t/"
echo [Run snack-db]
sudo rm -f ~/snack/db/mongod.lock # remove old lock
docker run -d --name snack-db -p 27017:27017 -p 28017:28017 -v ~/snack/db:/data/db -e AUTH=no snackwatcher/snack-db
echo [Run snack-web]
docker run -d --name snack-web -p 80:8000 -v snack-web:/opt/snack/SnackWatcher/static/images --link snack-db:snack-db snackwatcher/snack-web
