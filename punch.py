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
import struct

def bytes2addr( bytes ):
    """Convert a hash to an address pair."""
    if len(bytes) != 6:
        raise ValueError, "invalid bytes"
    host = socket.inet_ntoa( bytes[:4] )
    port, = struct.unpack( "H", bytes[-2:] )
    return host, port

def connect(pool, master):

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
    print >> sys.stderr, "connected to %s:%d" % target

    return target, sockfd


# vim: expandtab shiftwidth=4 softtabstop=4 textwidth=79:
