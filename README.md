cloudcraft
==========

Easy minecraft server management on the cloud.
This is a toolbelt to manage minecraft server instances. The tool is still under development but should be stable enough to work.

Installation
-

```$ pip install -r requirements.txt```

Quickstart
-

`spawn` spins up instances, creates keypairs and authorizes security groups for minecraft automatically.

    $ ./cloudcraft spawn myserver
    INFO: Spawning instance foobar. This will take a couple of minutes...
    INFO: Instance foobar is up and running. Run 'setup' to install minecraft


`setup` fetches the latest minecraft_server.jar and starts the server.

    $ ./cloudcraft setup myserver
    ...
    ...
    Starting minecraft server
    Started minecraft server successfully! Connect to '50.112.23.3' for Multiplayer
    Happy mining!


That's it! :)


More commands
-

### Listing instances
    $ ./cloudcraft list
    myserver


### Get details about an instance
    $ ./cloudcraft list myserver


### Stop the minecraft server
    $ ./cloudcraft stop myserver
    Running 'stop' for 'myserver'
    -------
    Warning miners...
    Saving map...
    Stopping server...


### Starting minecraft server
    $ ./cloudcraft start myserver
    Running 'start' for 'myserver'
    -------
    Starting minecraft server
    Started minecraft server successfully! Connect to '50.112.23.3' for Multiplayer
    Happy mining!

### Saving the map
    $ ./cloudcraft save myserver
    Running 'save' for 'myserver'
    -------
    Saving map...


### Get logs
    $ ./cloudcraft logs myserver
    ...
    ...
    2013-05-26 18:24:01 [INFO] Saving worlds
    2013-05-26 18:24:01 [INFO] Saving chunks for level 'world'/Overworld
    2013-05-26 18:24:49 [INFO] Starting minecraft server version 1.5.2
    2013-05-26 18:24:49 [INFO] Loading properties
    2013-05-26 18:24:49 [INFO] Default game type: SURVIVAL
    2013-05-26 18:24:49 [INFO] Generating keypair
    2013-05-26 18:24:50 [INFO] Starting Minecraft server on *:25565
    2013-05-26 18:24:50 [INFO] Preparing level "world"
    2013-05-26 18:24:50 [INFO] Preparing start region for level 0
    2013-05-26 18:24:51 [INFO] Preparing spawn area: 35%
    2013-05-26 18:24:52 [INFO] Done (1.984s)! For help, type "help" or "?"


### Login to the instance
    $ ./cloudcraft sh myserver


### Destroy the EC2 instance
    $ ./cloudcraft destroy myserver



TODO
-

- Implement EC2 scaling to save costs
- `setup.py` script for proper distribution
- plugin management
- Manage multiple instances of minecraft_server.jar
- More documentation
- Keep track of instance shutdowns. If an instance is shutdown
- Test cases


Thanks
-
[Mojang](http://mojang.com/) for an awesome game!
