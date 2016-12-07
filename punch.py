#!/usr/bin/env python
#
# Proof of Concept: UDP Hole Punching
# Two client connect to a server and get redirected to each other.
#
# This is the client.
#
# Koen Bollen <meneer koenbollen nl>
# 2010 GPL
#

import sys
import socket
from select import select
import struct
import time

import VLCSync

def bytes2addr( bytes ):
    """Convert a hash to an address pair."""
    if len(bytes) != 6:
        raise ValueError, "invalid bytes"
    host = socket.inet_ntoa( bytes[:4] )
    port, = struct.unpack( "H", bytes[-2:] )
    return host, port

def punch(isSim = False):
    try:
        master = (sys.argv[1], int(sys.argv[2]))
        pool = sys.argv[3].strip()
    except (IndexError, ValueError):
        print >> sys.stderr, "usage: %s <host> <port> <pool>" % sys.argv[0]
        sys.exit(65)

    sockfd = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
    sockfd.sendto( pool, master )
    data, addr = sockfd.recvfrom( len(pool)+3 )
    if data != "ok "+pool:
        print >> sys.stderr, "unable to request!"
        sys.exit(1)
    sockfd.sendto( "ok", master )
    print >> sys.stderr, "request sent, waiting for partner in pool '%s'..." % pool
    data, addr = sockfd.recvfrom( 6 )

    target = bytes2addr(data)
    print >>sys.stderr, "connected to %s:%d" % target

    #Connection Established

    username = ""
    password = "1234"
    ip = "localhost"
    pool = "10"

    local = VLCSync.VLC(ip, password)

    localStatus = "stopped"
    remoteStatus = "stopped"

    while True:
        # sockfd.sendto("asdadadssad", target)
        rfds,_,_ = select([sockfd], [], [], 1)
        # print rfds
        if sockfd in rfds:
            print "if"
            data, addr = sockfd.recvfrom(1024)
            data = data.strip()
            # print "data : " + data
            if (data[0] == "~"):
                print "helloooooo :)"
            remoteStatus = local.sync(data, remoteStatus, isSim)
            sys.stdout.flush()  

        else:
            # print "nop"
            print "else"
            data = local.getStatus()
            changed = False
            if (localStatus != data):
                data = "~" + data
                changed = True

            try :
                # print "send : " + data + " to %s:%d " % target
                sockfd.sendto(data, target)
            except:
                print "Could not send data !"

            if changed:
                localStatus = data[1:]
            else:
                localStatus = data

        time.sleep(1)


    sockfd.close()

if __name__ == "__main__":
    punch()

# vim: expandtab shiftwidth=4 softtabstop=4 textwidth=79:
