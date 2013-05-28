import json
import os

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


    

    
            
        
        
        
    
