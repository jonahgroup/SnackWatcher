#!/usr/bin/env bash
# http://docs.mongodb.org/manual/tutorial/install-mongodb-on-ubuntu/

echo ------------------------------------------- RESET MONGODB

echo 1. Reset all databases in MongoDB
mongo --eval "var m=db.getMongo(); m.getDBNames().forEach(function(name) { print('drop '+name); m.getDB(name).dropDatabase() });"

echo ------------------------------------------- RESET MONGODB - COMPLETE
