import boto.ec2 as ec2

def __get_connection(token, secret, region):
    conn = ec2.connect_to_region(region, aws_access_key_id=token,
                                 aws_secret_access_key=secret)
    return conn


def provision(aws_access_token="", aws_access_secret="",
              ec2_region="us-west-2", ami="ami-bf1d8a8f",
              instance_type="m1.small"):
    instance = {}
    print "Provisioning instances"
    conn = __get_connection(aws_access_token, aws_access_secret,
                            ec2_region)
    return True

    
