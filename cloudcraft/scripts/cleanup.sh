source ./lib.sh
if pgrep -f "minecraft_server" > /dev/null
then
    echo "Warning miners."
    mc_command say "WARNING: We are nuking the server down in 10 seconds"
    echo "Saving map..."
    mc_command save-all
    # Maybe do a backup here
    sleep 10
    echo "Stopping minecraft server..."
    mc_command stop
    rm -rf ${mc_home}
else
    rm -rf ${mc_home}
fi
    

