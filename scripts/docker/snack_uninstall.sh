#!/bin/sh
# Remove all remnants of SnackWatcher
echo [UNINSTALL]
sh snack_reset.sh | sed "s/^/\t/"
echo [Remove snack-db]
docker rmi -f snackwatcher/snack-db
echo [Remove snack-web]
docker rmi -f snackwatcher/snack-web
