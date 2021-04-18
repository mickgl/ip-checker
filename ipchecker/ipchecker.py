#!/usr/bin/env python
#
# Copyright (c) 2021 michgl <michgl33s@gmail.com>
#
# IP Checker
# Tool to check currently connected IP using GreyNoise API.
#
# Version 1.2.1

import os
import sys
import requests
import subprocess
import time
import argparse
import site
from .conf import *

cmd = argparse.ArgumentParser(prog="ipchecker", description="IP Checker - scan connected IP using GreyNoise API")
cmd.add_argument("--log", help="save all IP's in text file, default '/var/log/ip-checker'", action='store_true')
cmd.add_argument("--no-background", help='perform one scan and exit', action='store_true')
cmd.add_argument("--cfg", help="access configuration file with your default text editor", action='store_true')
cmd.add_argument("--quiet", help="just like default but without notifications", action='store_true')
args = cmd.parse_args()


# Function which we will use to send notifications.
def notify():
    # Check if 'notify-send' installation exists.
    ns = subprocess.call(['notify-send', '--help'], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
    
    # Send notification if exists.
    if ns == 0:
        subprocess.run(['notify-send', '-t', '3', "IP-Checker", "Check out ip-checker running terminal"])

# Function will be used if 'paranoia' variable is set to 'high' in configuration file.
def high(r):
    print(r)

# Function will be used if 'paranoia' variable is set to 'medium' in configuration file.
def med(r):
    if '"riot": false' in r:
        print(r)
        if not args.quiet and not '"classification": "benign"':
            notify()

# Function will be used if 'paranoia' variable is set to 'low' in configuration file.
def low(r):
    if '"classification": "malicious"' in r:
        print(r)
        if not args.quiet:
            notify()

# Function which we will use to connect to API
def connect(service, ip):
    # Both 'service' and 'ip' variables are defined in configuration file.
    url = service + ip

    headers = {"Accept": "application/json"}
    response = requests.request("GET", url, headers=headers)

    # Depends on 'paranoia' variable from conf.py 'connect()' will push results of scan to predefined functions
    if paranoia == 'medium':
        med(response.text)
    elif paranoia == 'high':
        high(response.text)
    elif paranoia == 'low':
        low(response.text)
    else:
        print("Error, please check your conf.py!")
        sys.exit(1)

# Function will be used if given no arguments from command line.
def default():
    # Check if our OS is Linux/Unix
    if not os.name == 'posix':
        print("Your system is not supported")
        sys.exit(1)

    arg = '-anp' # Variable with argument for netstat.
    
    # Check if our os is BSD/macOS, if yes, change argument for netstat.
    nsarg = os.uname()
    if not 'Linux' in nsarg:
        arg = '-an'

    while True:
        # Get output about currently connected IP's from netstat
        n1 = subprocess.Popen(['netstat', arg], stdout=subprocess.PIPE) # Can be also '-tnp' if we want to look only for TCP connections or '-unp' for UDP connections. Feel free to change arguments for netstat.
        n2 = subprocess.Popen(['grep', 'ESTABLISHED'], stdin=n1.stdout, stdout=subprocess.PIPE) # Look only for established connections.
        n3 = subprocess.Popen(['grep', '-E', '-o', '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}'], stdin=n2.stdout, stdout=subprocess.PIPE) # Push pure IP addreses to output
        output = subprocess.check_output(['grep', '-v', '192.168'], stdin=n3.stdout) # Exclude connections inside local network

        # Output is by default in bytes, so we will change it to string
        ips = output.decode()
        # Push output to list
        pr = ips.split()

        # Check how many IP's we have in 'pr'
        n = len(pr)
        # Create variable that we will be using as index for 'pr'
        pp = 0

        # Check IP's using connect() until all IP's listed by netstat were checked
        for i in range(n):
            connect(api, pr[pp])    # Run connect() using 'api' provided by conf.py and first IP from 'pr'
            pp = pp + 1             # Upgrade our index

        # 'checktime' is defined in configuration file, and should be modifed by user, depending on how often IP Checker should repeat scan
        time.sleep(checktime)

# Function will be used if given '--no-background' from command line.
def no_background():
    # Check if our OS is Linux/Unix
    if not os.name == 'posix':
        print("Your system is not supported")
        sys.exit(1)

    arg = '-anp' # Variable with argument for netstat.
    
    # Check if our os is BSD/macOS, if yes, change argument for netstat.
    nsarg = os.uname()
    if not 'Linux' in nsarg:
        arg = '-an'

    # Get output about currently connected IP's from netstat
    n1 = subprocess.Popen(['netstat', arg], stdout=subprocess.PIPE) # Can be also '-tnp' if we want to look only for TCP connections or '-unp' for UDP connections. Feel free to change arguments for netstat.
    n2 = subprocess.Popen(['grep', 'ESTABLISHED'], stdin=n1.stdout, stdout=subprocess.PIPE) # Look only for established connections.
    n3 = subprocess.Popen(['grep', '-E', '-o', '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}'], stdin=n2.stdout, stdout=subprocess.PIPE) # Push pure IP addreses to output
    output = subprocess.check_output(['grep', '-v', '192.168'], stdin=n3.stdout) # Exclude connections inside local network

    # Output is by default in bytes, so we will change it to string
    ips = output.decode()
    # Push output to list
    pr = ips.split()

    # Check how many IP's we have in 'pr'
    n = len(pr)
    # Create variable that we will be using as index for 'pr'
    pp = 0

    # Check IP's using connect() until all IP's listed by netstat were checked
    for i in range(n):
        connect(api, pr[pp])    # Run connect() using 'api' provided by conf.py and first IP from 'pr'
        pp = pp + 1             # Upgrade our index

def with_logging():
    # Check if our OS is Linux/Unix
    if not os.name == 'posix':
        print("Your system is not supported")
        sys.exit(1)

    arg = '-anp' # Variable with argument for netstat.
    
    # Check if our os is BSD/macOS, if yes, change argument for netstat.
    nsarg = os.uname()
    if not 'Linux' in nsarg:
        arg = '-an'

    while True:
        # Get output about currently connected IP's from netstat
        n1 = subprocess.Popen(['netstat', arg], stdout=subprocess.PIPE) # Can be also '-tnp' if we want to look only for TCP connections or '-unp' for UDP connections. Feel free to change arguments for netstat.
        n2 = subprocess.Popen(['grep', 'ESTABLISHED'], stdin=n1.stdout, stdout=subprocess.PIPE) # Look only for established connections.
        n3 = subprocess.Popen(['grep', '-E', '-o', '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}'], stdin=n2.stdout, stdout=subprocess.PIPE) # Push pure IP addreses to output
        output = subprocess.check_output(['grep', '-v', '192.168'], stdin=n3.stdout) # Exclude connections inside local network

        # Output is by default in bytes, so we will change it to string
        ips = output.decode()
        # Push output to list
        pr = ips.split()

        # Check if log file selected in conf.py exists, if not create it.
        if os.path.exists(log):
            save = open(log, 'a+')
            save.write('\n' + ips)
            save.close()
        else:
            save = open(log, 'w')
            save.write('\n' + ips)
            save.close()

        # Check how many IP's we have in 'pr'
        n = len(pr)
        # Create variable that we will be using as index for 'pr'
        pp = 0

        # Check IP's using connect() until all IP's listed by netstat were checked
        for i in range(n):
            connect(api, pr[pp])    # Run connect() using 'api' provided by conf.py and first IP from 'pr'
            pp = pp + 1             # Upgrade our index

        # 'checktime' is defined in configuration file, and should be modifed by user, depending on how often IP Checker should repeat scan
        time.sleep(checktime)

def conf():
    edt = os.environ['EDITOR']
    cf = site.getusersitepackages() + "/ipchecker/conf.py"
    subprocess.run([edt, cf])

def main():
    # Check arguments from command line and then run with choosen argument.
    if args.log:
        with_logging()
    elif args.no_background:
        no_background()
    elif args.cfg:
        conf()
    # If no argument given, run program in default mode.
    else:
        default()
