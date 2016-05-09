#!/bin/sh
echo /// [STOP]
echo /// remove containers
docker ps -aq -f ancester=snack-db | xargs -r -I % docker rm -f %
docker ps -aq -f ancester=snack-web | xargs -r -I % docker rm -f %
