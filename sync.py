#!/usr/bin/python
import time
import sys
from getpass import getpass
from select import select

import VLC
import punch
import config

def main(isSim = False):
    try:
        pool = sys.argv[1].strip()

    except (IndexError, ValueError):
        print >> sys.stderr, "usage: %s <host> <port> <pool>" % sys.argv[0]
        sys.exit(65)
    
    #Connection Established
    conf = config.config()
    conf.configure()
    
    master = (conf.host, conf.port)

    target, sockfd = punch.connect(pool, master)

    local = VLC.VLC(conf.ip, conf.password)

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