SCREEN_ID="minecraft"

function mc_command
{
    local cmd=$1
    local args=$2
    local mc_cmd="$cmd $args"
    mc_cmd=`echo $mc_cmd | sed -e 's/^ *//g' -e 's/ *$//g'`
    screen -p 0 -s $SCREEN_ID -X eval "stuff \"${mc_cmd}\"\015"
}


function mc_save
{
    if pgrep -f "server" > /dev/null
    then
        echo "Saving map"
        echo "Going read-only..."
        mc_command say "Saving map..."
        mc_command save-off
        mc_command save-all
        sync
        echo "Going read-write..."
        mc_command save-on
    else
        echo "Minecraft server not running"
    fi
}


function mc_stop
{
    if pgrep -f "server" > /dev/null
    then
        echo "Warning miners..."
        mc_command say "WARNING: shutting down in 10 seconds"
        mc_save
        sleep 10
        echo "Stopping minecraft server..."
        mc_command stop
    else
        echo "Minecraft server already stopped"
    fi
}
