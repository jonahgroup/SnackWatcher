#!/bin/sh
echo /// [RESTART]
sh docker_stop.sh | sed "s/^/\t/"
echo /// run snack-db
docker run -d --name snack-db -p 27017:27017 -p 28017:28017 -e AUTH=no snackwatcher/snack-db
echo /// run snack-web
docker run -d --name snack-web -p 80:8000 --link snack-db:snack-db snackwatcher/snack-web
