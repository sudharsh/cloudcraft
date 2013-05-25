echo "Stopping minecraft server"
pkill -f minecraft_server.jar
pgrep minecraft_server || echo "Stopped server"

