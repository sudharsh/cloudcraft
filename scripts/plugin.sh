source ./lib.sh
command=${1}
plugin_url=${2}

plugin_dir=${mc_home}/plugins

[ -z $command ] && (echo "Command is mandatory"; exit -1)
[ -z $plugin_url ] && (echo "Plugin URL is mandatory"; exit -1)

case $command in
    install)
        echo "Downloading $plugin_url"
        mkdir -p ${plugin_dir}
        wget $plugin_url -O ${plugin_dir}/plugin.zip
        echo "Extracting archive"
        unzip -d ${plugin_dir} ${plugin_dir}/plugin.zip
        echo "Cleaning up"
        rm -rf ${plugin_dir}/plugin.zip
        ;;
    update)
        echo "Updating $plugin_url"
        mkdir -p ${plugin_dir}
        wget $plugin_url -P ${plugin_dir}/update/plugin.zip
        echo "Extracting archive"
        unzip -d ${plugin_dir} ${plugin_dir}/update/plugin.zip
        echo "Cleaning up"
        rm -rf ${plugin_dir}/plugin.zip
        ;;
    uninstall)
        echo "Not implemented yet"
        ;;
    *)
        echo "Invalid sub-command: ${command}"
        exit -1
        ;;
esac
