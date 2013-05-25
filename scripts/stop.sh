echo "Stopping minecraft server"
pkill -f minecraft_server.jar
pgrep minecraft_server || (echo "Server already stopped"; exit 1)
