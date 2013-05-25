from fabric.api import local, run, cd, put
from fabric.colors import green, red

import os
import StringIO
import traceback

REMOTE_PATH = "~/cloudcraft/"
BOOTSTRAP_PATH = "bootstrap/"
SCRIPTS_PATH = "scripts/"

def bootstrap_server(ami_id):
    run("mkdir -p %s" % REMOTE_PATH)
    cd(REMOTE_PATH)
    print(green("Bootstrapping %s" % ami_id))
    print(green("------"))
    try:
        put(BOOTSTRAP_PATH + ami_id + ".sh", REMOTE_PATH + "bootstrap.sh")
    except ValueError:
        print(red("Couldn't find bootstrap script for AMI:%s" % ami_d))
    run("sh {0}/bootstrap.sh".format(REMOTE_PATH), pty=False, combine_stderr=False)
    print(green("------"))



def run_remote(command, command_args=[], remote_vars={}):
    try:
        print(green("-------"))
        run("mkdir -p %s" % REMOTE_PATH)
        script_file = "{0}/{1}.sh".format(SCRIPTS_PATH, command)
        remote_path = "{0}/{1}.sh".format(REMOTE_PATH, command)
        prepared_buffer = StringIO.StringIO()
        for k, v in remote_vars.items():
            prepared_buffer.write('%s="%s"\n' %(k,v))
        with open(script_file, "r") as fh:
            prepared_buffer.write(fh.read())
        put(prepared_buffer, remote_path)
        with cd(REMOTE_PATH):
            return run("sh ./{0}.sh {1}".format(command, command_args), pty=False, combine_stderr=False)
        print(green("-------"))

    except ValueError, IOError:
        print(traceback.format_exc())
        print(red("Is the machine up?"))
        return
    except:
        print(red("Error when executing command {0}".format(command)))
        return