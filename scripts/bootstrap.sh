#!/usr/bin/env sh
# WARNING: This will be executed in the remote machine

echo "Installing Java"
sudo apt-get update
sudo apt-get install -y openjdk-7-jre-headless
echo "Done installing Java version 7"

echo "Creating directory for minecraft"
mkdir -p ~/minecraft
