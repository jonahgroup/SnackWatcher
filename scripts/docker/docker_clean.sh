#!/bin/sh
echo /// [CLEAN]
echo /// delete unused images
docker images -q -f dangling=true | xargs -r -I % docker rmi -f %
