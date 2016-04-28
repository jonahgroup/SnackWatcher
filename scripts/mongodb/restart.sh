#!/usr/bin/env bash
# http://docs.mongodb.org/manual/tutorial/install-mongodb-on-ubuntu/

echo ------------------------------------------- RESTART MONGODB

echo [0. Stop MongoDB]
sudo bash stop.sh | sed "s/^/\t/"

echo 1. Start MongoDB
sudo service mongod start

echo ------------------------------------------- RESTART MONGODB - COMPLETE
