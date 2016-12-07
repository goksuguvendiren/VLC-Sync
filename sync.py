#!/usr/bin/python
import time
import sys
from select import select

import VLC
import punch

def main(isSim = False):
    try:
        master = (sys.argv[1], int(sys.argv[2]))
        pool = sys.argv[3].strip()

    except (IndexError, ValueError):
        print >> sys.stderr, "usage: %s <host> <port> <pool>" % sys.argv[0]
        sys.exit(65)

    target, sockfd = punch.connect(pool, master)
    
    #Connection Established

    username = ""
    password = "1234"
    ip = "localhost"
    pool = "10"

    local = VLC.VLC(ip, password)

    localStatus = local.getStatus()
    remoteStatus = "stopped"

    while True:
        print localStatus
        rfds,_,_ = select([sockfd], [], [], 0.5)
        if sockfd in rfds:
            data, addr = sockfd.recvfrom(1024)
            data = data.strip()
            if (data[0] == "~"):
                remoteStatus = local.sync(data, remoteStatus, isSim)
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