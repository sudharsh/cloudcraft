source ./lib.sh
if pgrep -f "server" > /dev/null
then
    echo "Saving map..."
    mc_command say "Saving map..."
    mc_command save-all
else
    echo "Minecraft server not running"
fi
