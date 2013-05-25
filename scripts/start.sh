echo "Starting minecraft server" 1>&2
nohup java -Xms${ms} -Xmx${mx} -jar minecraft_server.jar nogui >> nohup.out &
echo $! > server.pid

(pgrep -F server.pid && echo "Started server :). Watch out for the creepers") || echo "Couldn't start the minecraft server. Use 'logs'"




