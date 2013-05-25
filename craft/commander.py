from fabric.api import local, run, cd, put
from fabric.colors import green, red

import os
import StringIO
import traceback

REMOTE_PATH = "~/cloudcraft/"
BOOTSTRAP_PATH = "bootstrap/"

def bootstrap_server(ami_id):
    run("mkdir -p %s" % REMOTE_PATH)
    cd(REMOTE_PATH)
    print(green("Bootstrapping %s" % ami_id))
    try:
        put(BOOTSTRAP_PATH + ami_id + ".sh", REMOTE_PATH + "bootstrap.sh")
    except ValueError:
        print(red("Couldn't find bootstrap script for AMI:%s" % ami_d))
    run("sh {0}/bootstrap.sh".format(REMOTE_PATH), pty=False, combine_stderr=False)


