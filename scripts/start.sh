if pgrep -f "minecraft_server" > /dev/null
then
    echo "Minecraft server already running"
else
    echo "Starting minecraft server"
    screen -dmS minecraft java -Xms${ms} -Xmx${mx} -jar minecraft_server.jar nogui
    pgrep -f "minecraft_server" > /dev/null || (echo "Couldn't start the minecraft server. Use 'logs'" && exit 1)
    ubip=$(curl http://ip4.me 2>/dev/null | sed -e 's#<[^>]*>##g' | grep '^[0-9]')
    echo "Started minecraft server successfully! Connect to '$ubip' for Multiplayer"
    echo "Happy mining!"
fi
