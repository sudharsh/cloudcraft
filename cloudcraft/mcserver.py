# Cloudcraft
# Copyright 2013, Sudharshan S
# See COPYING for more.

import subprocess
import json
import os

import fabric.context_managers as ctxt
from fabric.colors import green, red
from fabric.tasks import execute

import commander


def load_server(path):
    i = {}
    try:
        i = json.load(open(path))
    except IOError:
        return None
    args = []
    for a in ["server_id", "name", "user"]:
        args.append(i.pop(a))
    ms = MinecraftServer(*args, **i)
    return ms


def save_server(server, path):
    fh = open(os.path.join(path), "w")
    fh.write(str(server))
    

class MinecraftServer(object):

    def __init__(self, server_id, name, user,
                 server_version="https://s3.amazonaws.com/MinecraftDownload/launcher/minecraft_server.jar",
                 **kwargs
                 ):
        self.server_id = server_id
        self.name = name
        self.user = user
        self.plugins = []
                

    def __repr__(self):
        return json.dumps(self.__dict__, indent=True)


    def run_command(self, host,
                    command, key_file, command_args=[],
                    remote_vars={}):
        host_string = "{0}@{1}".format(self.user, host)
        commands = [command] if isinstance(command, basestring) else command
        with ctxt.settings(
            host_string=host_string,
            key_filename=key_file,
            output_prefix=False):
            with ctxt.hide("running", "aborts"):
                for cmd in commands:
                    if cmd in ["sh", "shell"]:
                        print(green("Logging in as '%s'" % self.user))
                        subprocess.call(["ssh", "-i", key_file, "%s" % (host_string)])
                    else:
                        print(green("----- Running '{0}' on '{1}' -----".format(cmd, self.name)))

                        res = execute(commander.run_remote, cmd, command_args=command_args,
                                      remote_vars=remote_vars)
                        print(green("----- Done '{0}' on '{1}' -----".format(cmd, self.name)))
        return True


                    
                
        
        
        
    


    

    
            
        
        
        
    
