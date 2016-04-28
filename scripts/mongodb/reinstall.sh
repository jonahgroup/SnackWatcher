#!/usr/bin/env bash
# UBUNTU 12.04 only
# http://docs.mongodb.org/manual/tutorial/install-mongodb-on-ubuntu/

echo =========================================== REINSTALL MONGODB

echo [0. Uninstall]
sudo bash uninstall.sh | sed "s/^/\t/"

echo 1. Import the public key used by the package management system
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10

echo 2. Create a list file for MongoDB
echo "deb http://repo.mongodb.org/apt/ubuntu precise/mongodb-org/3.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.0.list

echo 3. Reload local package database
sudo apt-get update

echo 4. Install the MongoDB packages
sudo apt-get install -y mongodb-org

echo =========================================== REINSTALL MONGODB - COMPLETE
