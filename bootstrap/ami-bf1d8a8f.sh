#!/usr/bin/env sh
# WARNING: This will be executed in the remote machine

echo "Installing Java" 1>&2
sudo apt-get update
sudo apt-get install -y openjdk-7-jdk
echo "Done installing Java version 7" 1>&2

