SCREEN_ID="minecraft"

function mc_command
{
    local cmd=$1
    local args=$2
    local mc_cmd="$cmd $args"
    mc_cmd=`echo $mc_cmd | sed -e 's/^ *//g' -e 's/ *$//g'`
    screen -p 0 -s $SCREEN_ID -X eval "stuff \"${mc_cmd}\"\015"
}
