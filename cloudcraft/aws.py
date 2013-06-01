# Cloudcraft
# Copyright 2013, Sudharshan S
# See COPYING for more.

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
        return None


    def sync_keypair(self, key_name, path):
        """Creates and syncs the keypair"""
        log.debug("Syncing {0} from {1}".format(key_name, self.region))
        key_path = os.path.join(path, "{0}.pem".format(key_name))
        try:
            key = self.conn.create_key_pair(key_name)
            key.save(path)
        except:
            if not os.path.exists(key_path):
                log.error("AWS Key {0}.pem was already generated but cloudcraft couldn't find the private key in {1}".format(key_name, path))
                log.error("You have the following choices")
                log.error("1.) Copy '{0}.pem' to '{1}' if you have the keyfile somewhere".format(key_name, path))
                log.error("2.) If you have lost '{0}.pem', delete '{0}' from your AWS Keypairs management console. Cloudcraft will sync the private key on the next run".format(key_name))
                log.error("3.) Give your own keyfile in the cloudcraft config. You must copy the corresponding private key in {0}.".format(path))
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
        if m:
            log.info("Terminating instance %s", m.id)
            m.terminate()
            return True
        return False


    def shutdown(self, mcserver):
        m = self.get_instance(mcserver.server_id)
        if m:
            log.info("Stopping instance %s", m.id)
            m.stop()
            return True
        return False


    def boot(self, mcserver):
        m = self.get_instance(mcserver.server_id)
        if m:
            log.info("Booting up instance %s", m.id)
            m.start()
            return True
        return False


    def reboot(self, mcserver):
        m = self.get_instance(mcserver.server_id)
        if m:
            log.info("Rebooting instance %s", m.id)
            m.reboot()
            return True
        return False


    def info(self, mcserver):
        m = self.get_instance(mcserver.server_id)
        if not m:
            return False
        print "----- Machine Status for {0} -----".format(mcserver.name)
        data = {}
        for k in ["public_dns_name", "state"]:
            data[k] = getattr(m, k)
        for k in ["plugins"]:
            data[k] = getattr(mcserver, k)
        for k, v in data.items():
            print "{0}: {1}".format(k, v)
        return True
