source ./lib.sh
if pgrep -f "minecraft_server" > /dev/null
then
    echo "Warning miners..."
    mc_command say "WARNING: shutting down in 10 seconds"
    echo "Saving map..."
    mc_command save-all
    sleep 10
    echo "Stopping server..."
    mc_command stop
else
    echo "Server already stopped"
fi
