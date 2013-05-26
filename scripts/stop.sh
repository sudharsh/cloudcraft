if pgrep -f "minecraft_server" > /dev/null
then
    echo "Warning miners..."
    screen -p 0 -S minecraft -X eval 'stuff "say WARNING: Server shutting down in 10 seconds"\015'
    echo "Saving map..."
    screen -p 0 -S minecraft -X eval 'stuff "save-all"\015'
    sleep 10
    echo "Stopping server..."
    screen -p 0 -S minecraft -X eval 'stuff "stop"\015'
else
    echo "Server already stopped"
fi
