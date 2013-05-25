echo "Starting minecraft server" 1>&2
nohup java -Xms${ms} -Xmx${mx} -jar minecraft_server.jar nogui >> nohup.out &
echo $! > server.pid

pgrep -F server.pid || (echo "Couldn't start the minecraft server. Use 'logs'" && exit 1)

ubip=$(curl http://ip4.me 2>/dev/null | sed -e 's#<[^>]*>##g' | grep '^[0-9]')

echo "Started minecraft server successfully! Connect to '$ubip' for Multiplayer"
echo "Happy mining!"
