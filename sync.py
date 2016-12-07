#!/usr/bin/python
import time
import sys
import json
import os.path
from getpass import getpass
from select import select

import VLC
import punch

def configuration():
    username = ""
    password = ""
    ip = "localhost"

    if not os.path.isfile("config.json"):
        username = raw_input("Username: ")
        password = getpass('Password: ')
        ip = raw_input("Ip: ")

        data = {"username": username, "password": password, "ip": ip}

        with open("config.json", "w") as config:
            json.dump(data, config, sort_keys = True, indent = 4,)

    with open("config.json", "r") as config:
        data = json.load(config)

    username = data["username"]
    password = data["password"]
    ip       = data["ip"]

    return username, password, ip

def main(isSim = False):
    try:
        master = (sys.argv[1], int(sys.argv[2]))
        pool = sys.argv[3].strip()

    except (IndexError, ValueError):
        print >> sys.stderr, "usage: %s <host> <port> <pool>" % sys.argv[0]
        sys.exit(65)

    target, sockfd = punch.connect(pool, master)
    
    #Connection Established
    
    username, password, ip = configuration()

    local = VLC.VLC(ip, password)

    localStatus = local.getStatus()
    remoteStatus = "stopped"

    while True:
        rfds,_,_ = select([sockfd], [], [], 0.5)
        if sockfd in rfds:
            data, addr = sockfd.recvfrom(1024)
            data = data.strip()
            if (data[0] == "~"):
                localStatus = local.sync(data[1:], remoteStatus, isSim)
            sys.stdout.flush()

        else:
            data = local.getStatus()
            changed = False
            if (localStatus != data):
                data = "~" + data
                changed = True

            try :
                sockfd.sendto(data, target)
            except:
                print "Could not send data !"

            if changed:
                localStatus = data[1:]
            else:
                localStatus = data

        time.sleep(0.5)


    sockfd.close()

if __name__ == "__main__":
    main()