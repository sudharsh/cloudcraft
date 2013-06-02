source ./lib.sh

function mc_archive
{
    archive_name="archive_${server_name}_`date +%Y%m%d_%H%M`.tar.gz"
    pushd ~ > /dev/null
    tar -cvf ~/.cloudcraft/${archive_name} `basename ${mc_home}`
    rm -f ~/.cloudcraft/latest_archive
    ln -s ~/.cloudcraft/${archive_name} ~/.cloudcraft/latest_archive
    popd > /dev/null
}

if pgrep -f "server" > /dev/null
then
    echo "Warning miners"
    mc_command say "NOTICE: Server being archived. Hang tight"
    echo "Going read-only"
    mc_save
    mc_command save-off
    sync
    echo "Waiting for the map to save..."
    sleep 10
fi

echo "------"
mc_archive
echo "------"
echo "Archived at ${archive_name}"

if pgrep -f "server" > /dev/null
then
    echo "Going read-write mode..."
    mc_command save-on
fi
