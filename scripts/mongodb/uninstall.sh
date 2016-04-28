#!/usr/bin/env bash
# UBUNTU 12.04 only
# http://docs.mongodb.org/manual/tutorial/install-mongodb-on-ubuntu/

echo =========================================== UNINSTALL MONGODB

echo [0. Stop MongoDB]
sudo bash stop.sh | sed "s/^/\t/"

echo 1. Remove Packages
sudo apt-get -qq -y purge mongodb-org*

echo 2. Remove Data Directories
sudo rm -r /var/log/mongodb
sudo rm -r /var/lib/mongodb

echo =========================================== UNINSTALL MONGODB - COMPLETE
