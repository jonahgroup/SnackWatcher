#!/bin/sh
# Checkout the scripts from Git and download and run the SnackWatcher docker containers
echo [SNACK]
echo [Remove any existing clones]
rm -rf SnackWatcher
echo [Clone a fresh copy of SnackWatcher]
git clone --depth 1 https://github.com/jonahgroup/SnackWatcher.git
echo [Run SnackWatcher]
echo [Note: If this fails due to a Docker related issue, try running "sh docker_build.sh" and execute this script again]
sh SnackWatcher/scripts/docker/docker_run.sh | sed "s/^/\t/"
