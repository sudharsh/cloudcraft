command=${1}
echo $command
if [ $command == "tail" ]
then
    tail -n 50 -f ${mc_home}/server.log
else
    tail -n 50 ${mc_home}/server.log
fi
