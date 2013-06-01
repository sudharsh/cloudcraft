cloudcraft
==========

Easy minecraft server management on the cloud.
This is a toolbelt to manage minecraft server instances. The tool is still under development but should be stable enough to work.

Installation
-

### Using pip

`$ pip install cloudcraft`

If using Ubuntu, run `sudo apt-get install python-dev` before installing cloudcraft.


Quickstart
-

`spawn` spins up instances, creates keypairs and authorizes security groups for minecraft automatically.

    $ cloudcraft spawn myserver
    INFO: Spawning a 'ami-bf1d8a8f' 't1.micro' instance in region 'us-west-2'
    INFO: You can change these settings in '/Users/sudharsh/.cloudcraft/cloudcraft.conf'

    Continue? (y/n) [n]: y
    INFO: Spawning 'mcserver'. This will take a couple of minutes...
    INFO: Instance mcserver is up and running.


`setup` fetches the latest bukkit server and starts the server.

    $ cloudcraft setup myserver
    ...
    ...
    Starting minecraft server
    Started minecraft server successfully! Connect to '50.112.23.3' for Multiplayer
    Happy mining!


That's it! :)

For more commands, `cloudcraft -h`

### Minecraft server commands
    start SERVER
    stop SERVER
    save SERVER
    logs SERVER    - Print the minecraft server logs
    cleanup SERVER - Stop the server and remove the minecraft directory

### Bukkit plugin management
    plugin SERVER install URL      - Installs plugin at URL
    plugin SERVER uninstall PLUGIN - <Not Implemented yet>
    plugin SERVER update URL       - Update plugin from URL

### Machine commands
    shutdown SERVER
    reboot SERVER
    boot SERVER
    destroy SERVER - Terminates the EC2 instance
    info SERVER    - Dumps the current machine and minecraft installation status

### Others
    bootstrap SERVER - Bootstraps the SERVER for use (e.g, installation of Java)
    list keys|instances - Lists the keys and the instances.


TODO
-

- Implement EC2 scaling to save costs
- plugin management
- Manage multiple instances of minecraft_server.jar
- More documentation
- Test cases


Thanks
-
[Mojang](http://mojang.com/) for an awesome game!
