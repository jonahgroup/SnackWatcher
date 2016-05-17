#!/bin/sh
echo [RUN]
sh docker_stop.sh | sed "s/^/\t/"
echo [Run snack-db]
docker run -d --name snack-db -p 27017:27017 -p 28017:28017 -e AUTH=no snackwatcher/snack-db
echo [Run snack-web]
docker run -d --name snack-web -p 80:8000 -v ~/snack/static/images:/snack/static/images --link snack-db:snack-db snackwatcher/snack-web
echo [SnackWatcher should be running now!]
