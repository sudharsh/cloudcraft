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
        log.info("Terminating instance %s", m.id)
        return m.terminate()


    def shutdown(self, mcserver):
        m = self.get_instance(mcserver.server_id)
        log.info("Stopping instance %s", m.id)
        return m.stop()


    def boot(self, mcserver):
        m = self.get_instance(mcserver.server_id)
        log.info("Booting up instance %s", m.id)
        return m.start()


    def reboot(self, mcserver):
        m = self.get_instance(mcserver.server_id)
        log.info("Rebooting instance %s", m.id)
        return m.reboot()


    def info(self, mcserver):
        m = self.get_instance(mcserver.server_id)
        print "----- Machine Status for {0} -----".format(mcserver.name)
        data = {}
        for k in ["public_dns_name", "state"]:
            data[k] = getattr(m, k)
        for k in ["plugins"]:
            data[k] = getattr(mcserver, k)
        for k, v in data.items():
            print "{0}: {1}".format(k, v)
