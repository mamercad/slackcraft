#!/usr/bin/python

from __future__ import print_function
import argparse
import requests
import socket
import subprocess
import sys
import time

parser = argparse.ArgumentParser(description='Minecraft rcon to Slack')
parser.add_argument('--slackhook', help='Your Slack incoming webook URL', default='https://hooks.slack.com/services/XXX/XXX/XXX')
parser.add_argument('--mcrcon', help='Path to the mcrcon utility (GitHub-Tiiffi/mcrcon)', default='/home/minecraft/mcrcon/mcrcon')
parser.add_argument('--hostname', help='Minecraft rcon hostname', default='localhost')
parser.add_argument('--port', type=int, help='Minecraft server rcon', default=25575)
parser.add_argument('--password', help='Minecraft rcon password', default='password')
parser.add_argument('--sleep', type=int, help='Sleep interval (secs)', default=60)
args = parser.parse_args()

last_payload = None
while True:
    rcon_output = None
    try:
        rcon_output = subprocess.check_output("{0} -c -H {1} -P {2} -p {3} list; exit 0".format(
            args.mcrcon, args.hostname, args.port, args.password
        ), shell=True)
    except subprocess.CalledProcessError as e:
        print(e)
        sys.exit(1)
    if rcon_output:
        payload = {
            "text": "[{0}]{1}".format(socket.gethostname(), rcon_output),
            "attachements": {
                "text": "https://github.com/mamercad/slackcraft/"
            }
        }
        if last_payload != payload:
            print("Sending '[{0}]{1}' to Slack".format(socket.gethostname(), rcon_output.rstrip()))
            r = requests.post(args.slackhook, json=payload)
            last_payload = payload
    print("Sleeping for {0} seconds".format(args.sleep))
    time.sleep(args.sleep)
