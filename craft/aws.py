import logging
import time
import os
import traceback

from itertools import chain

import boto.ec2 as ec2
import boto.exception

import mcserver
import commander

log = logging.getLogger("cloudcraft")
logging.getLogger('boto').setLevel(logging.CRITICAL)


class AWS(object):

    def __init__(self, token, secret,
                 region="us-east-1"):
        self.region = region
        self.conn = ec2.connect_to_region(region, aws_access_key_id=token,
                                          aws_secret_access_key=secret)


    def get_instance(self, instance_id):
        reservations = self.conn.get_all_instances(instance_ids=[instance_id])
        machines = list(chain.from_iterable([i.instances for i in reservations]))
        for m in machines:
            if m.id == instance_id:
                return m
        return m


    def sync_keypair(self, key_name, path):
        """Creates and syncs the keypair"""
        log.debug("Syncing {0} from {1}".format(key_name, self.region))
        key_path = os.path.join(path, "{0}.pem".format(key_name))
        try:
            key = self.conn.create_key_pair(key_name)
            key.save(path)
        except:
            if not os.path.exists(key_path):
                log.error("AWS Key {0}.pem already generated but couldn't find it in {1}".format(key_name, path))
                log.error("This usually means that the keyfile was deleted locally.")
                log.error("Generate the keypair manually and place {0}.pem in {1}".format(key_name, path))
                return None
            else:
                log.debug("Found {0}.pem. Keys are in sync".format(key_name))
        return key_path


    def sync_security_group(self, security_group):
        log.debug("Authorizing security group for minecraft")
        sec_groups = [x for x in self.conn.get_all_security_groups() if x.name == security_group]
        sec_group = None
        if not sec_groups:
            log.debug("Creating security group %s", security_group)
            sec_group = self.conn.create_security_group(security_group, "Minecraft server security group")
        else:
            sec_group = sec_groups[0]
        ports = [25565, 22] # minecraft and ssh
        existing_rules = [int(x.from_port) for x in sec_group.rules]
        for p in ports:
            if p in existing_rules:
                log.debug("Port %s already open", p)
            else:
                log.debug("Opening up port %s", p)
                sec_group.authorize('tcp', p, p, '0.0.0.0/0')
        

    def spawn(self, name, ami=None, instance_type="t1.micro",
              key_name="cloudcraft", security_group="cloudcraft",
              user="root"):
        image = self.conn.get_image(ami)
        res = image.run(1, 1, instance_type=instance_type,
                       key_name=key_name, security_groups=["default", security_group])
        machine = res.instances[0]
        log.info("Spawning '{0}'. This will take a couple of minutes...".format(name))
        while machine.update() == "pending":
            time.sleep(2)
        log.debug("Instance state changed from 'pending' to {0}".format(machine.state))
        if machine.state != 'running':
            log.error("Couldn't start instance {0}. Please destroy the stale instance by logging in to your AWS console. This will be fixed in the future".format(machine.id))
            return None
        
        mcs = mcserver.MinecraftServer(machine.id, name,
                                       user, machine.public_dns_name)
        return mcs


    def destroy(self, mcserver):
        m = self.get_instance(mcserver.server_id)
        log.debug("Terminating instance %s", m.id)
        return m.terminate()


    def shutdown(self, mcserver):
        m = self.get_instance(mcserver.server_id)
        log.debug("Stopping instance %s", m.id)
        return m.stop()


    def boot(self, mcserver):
        m = self.get_instance(mcserver.server_id)
        log.debug("Booting up instance %s", m.id)
        return m.start()


    def reboot(self, mcserver):
        m = self.get_instance(mcserver.server_id)
        log.debug("Rebooting instance %s", m.id)
        return m.reboot()

     
        
                
    
        
"""
def __save_keypair(conn, keyname, path):
    # FIXME: This is rather naive. Handle this a bit smartly
    key_root = os.path.join(path, "keys")
    key_path = os.path.join(key_root, "{0}.pem".format(keyname))
    try:
        key = conn.create_key_pair(keyname)
        key.save(key_root)
    except:
        if not os.path.exists(key_path):
            log.error("AWS Key {0}.pem already generated but couldn't find it in {1}".format(keyname, key_root))
            log.error("This usually means that the keyfile was deleted locally.")
            log.error("Generate the keypair manually and place {0}.pem in {1}".format(keyname, key_root))
            return None
        else:
            log.debug("Found {0}.pem.".format(keyname))
    return key_path


def __delete_keypair(conn, keyname):
    conn.delete_key_pair(keyname)
    # Delete from disk as well

    
def provision(cloudcraft_home, name, aws_access_token="", aws_access_secret="",
              ec2_region="us-west-2", ami="ami-bf1d8a8f",
              instance_type="m1.small", keyname=None, security_group=None):
    instance_metadata = {}
    instance_metadata["mcs_name"] = name
    conn = __get_connection(aws_access_token, aws_access_secret,
                            ec2_region)

    if not keyname:
        keyname = "cloudcraft-{0}".format(ec2_region)
        log.debug("Creating Keypair - {0}".format(keyname))
        keypair = __save_keypair(conn, keyname, cloudcraft_home
        if not keypair:
            return {}

    if not security_group:
        log.debug("Authorizing security group for minecraft")
        security_group = "cloudcraft"
        sec_groups = [x for x in conn.get_all_security_groups() if x.name == security_group]
        if not sec_groups:
            log.debug("Creating security group %s", security_group)
            sec_group = conn.create_security_group(security_group, "Minecraft server security group")
        else:
            sec_group = sec_groups[0]
        ports = [25565, 22] # minecraft and ssh
        existing_rules = [int(x.from_port) for x in sec_group.rules]
        for p in ports:
            if p in existing_rules:
                log.debug("Port %s already open", p)
            else:
                log.debug("Opening up port %s", p)
                sec_group.authorize('tcp', p, p, '0.0.0.0/0')
    
    image = conn.get_image(ami)
    res = image.run(1, 1, instance_type=instance_type,
              key_name=keyname, security_groups=["default", security_group])
    machine = res.instances[0]
    log.info("Spawning instance {0}. This will take a couple of minutes...".format(instance_metadata["mcs_name"]))
    while machine.update() == "pending":
        time.sleep(2)
    log.debug("Instance state %s", machine.state)
    if machine.state != "running":
        log.error("Couldn't start instance {0}. Please destroy the stale instance by logging in to your AWS console. This will be fixed in the future".format(machine.id))
        return {}

    for k in ["id", "private_ip_address", "image_id", "public_dns_name"]:
        instance_metadata[k] = getattr(machine, k)
    instance_metadata["keyname"] = keyname
    instance_metadata["security_group"] = security_group
    return instance_metadata


def destroy(instance, aws_access_token="", aws_access_secret="",
            ec2_region="us-west-2"):
    conn = __get_connection(aws_access_token, aws_access_secret,
                            ec2_region)
    machine_id = instance["id"]
    machines = list(chain.from_iterable([i.instances for i in conn.get_all_instances(instance_ids=[machine_id])]))
    log.error("%s not found or already terminated. Are you sure if it exists?" % (machine_id))
    return False

"""
