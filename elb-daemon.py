#!/usr/bin/env python3
import signal
import sys
import boto.ec2.elb
import argparse
import time

parser = argparse.ArgumentParser(description='Register the this CoreOS instance with the ELB, then deregister on exit')
parser.add_argument('lbname', metavar='<NAME>',
                    help='Name of AWS ELB that should be used for registration')
command_args = parser.parse_args()

conn = boto.ec2.elb.ELBConnection()

def instance_metadata():
    metadata = boto.utils.get_instance_metadata(timeout=2, num_retries=2)
    if not metadata:
        raise RuntimeError("Could not get instance metadata, "
                           "is this even an EC2 instance?")
    return metadata

def current_instance():
    return instance_metadata()['instance-id']

def deregister_from_elb(*args, **kwargs):
    conn.deregister_instances(command_args.lbname, current_instance())
    sys.exit(0)

def run():
    signal.signal(signal.SIGTERM, deregister_from_elb)
    signal.signal(signal.SIGINT, deregister_from_elb)
    conn.register_instances(command_args.lbname, current_instance())
    while True:
        time.sleep(5)

run()
