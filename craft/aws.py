import time
import os
import traceback

import boto.ec2 as ec2
import boto.exception

def __get_connection(token, secret, region):
    conn = ec2.connect_to_region(region, aws_access_key_id=token,
                                 aws_secret_access_key=secret)
    return conn


def __save_keypair(conn, keyname):
    # FIXME: This is rather naive. Handle this a bit smartly
    key = conn.create_key_pair(keyname)
    try:
        key.save(os.getcwdu())
    except boto.exception.EC2ResponseError:
        print "Keypair {0} already exists for region.".format(keyname)
        return None
    return os.path.join(os.getcwdu(), "{0}.pem".format(keyname))


def __delete_keypair(conn, keyname):
    conn.delete_key_pair(keyname)


def provision(aws_access_token="", aws_access_secret="",
              ec2_region="us-west-2", ami="ami-bf1d8a8f",
              instance_type="m1.small", keyname=None, security_group=None):
    instance_metadata = {}
    conn = __get_connection(aws_access_token, aws_access_secret,
                            ec2_region)

    if not keyname:
        keyname = "cloudcraft-{0}".format(ec2_region)
        print "Creating Keypair - {0}".format(keyname)
        keypair = __save_keypair(conn, keyname)
    # else: get keypair and save it to disk

    if not security_group:
        print "Opening up ports for minecraft server"
        security_group = "cloudcraft"
        sec_groups = conn.get_all_security_groups(groupnames=[security_group])
        if not sec_groups:
            print "Creating security group", security_group
            sec_group = conn.create_security_group(security_group, "Minecraft server security group")
        else:
            sec_group = sec_groups[0]
        try:
            sec_group.authorize('tcp', 25565, 25565, '0.0.0.0/0')
        except boto.exception.EC2ResponseError:
            print traceback.format_exc()

    image = conn.get_image(ami)
    res = image.run(1, 1, instance_type=instance_type,
              key_name=keyname, security_groups=["default", security_group])
    machine = res.instances[0]
    print "Provisioning instance", machine.id
    while machine.update() == "pending":
        time.sleep(2)
    print "Instance state", machine.state
    if machine.state != "running":
        print "Couldn't start instance {0}. Please destroy the stale instance by logging in to your AWS console. This will be fixed in the future".format(machine.id)
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
    __delete_keypair(conn)
