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

    $ ./cloudcraft spawn my_server
    INFO: Spawning instance foobar. This will take a couple of minutes...
    INFO: Instance foobar is up and running. Run 'setup' to install minecraft


`setup` fetches the latest minecraft_server.jar and starts the server.

    $ ./cloudcraft setup my_server
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
    my_server


### Get details about an instance
    `$ ./cloudcraft list my_server`


### Stop the minecraft server
    $ ./cloudcraft stop my_server
    Running 'stop' for 'mc'
    -------
    Warning miners...
    Saving map...
    Stopping server...


### Starting minecraft server
    $ ./cloudcraft start my_server
    Running 'start' for 'mc'
    -------
    Starting minecraft server
    Started minecraft server successfully! Connect to '50.112.23.3' for Multiplayer
    Happy mining!

### Saving the map
    $ ./cloudcraft save my_server
    Running 'save' for 'mc'
    -------
    Saving map...


### Get logs
    $ ./cloudcraft logs my_server
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
    $ ./cloudcraft sh my_server


### Destroy the EC2 instance
    $ ./cloudcraft destroy my_server



TODO
-

- Implement EC2 scaling to save costs
- `setup.py` script for proper distribution
- plugin management
- Manage multiple instance of minecraft_server.jar
- More documentation
- Keep track of instance shutdowns. If an instance is shutdown
- Test cases


Thanks
-
[Mojang](http://mojang.com/) for an awesome game!
