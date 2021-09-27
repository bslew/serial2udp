#!/usr/bin/env python3
import sys, time
import os
from socket import *



#
# process cmd params
#
#print sys.argv
def usage():
    print("USAGE: sendUDP.py 'string'  port [IP=127.0.0.1]")
    print("Example: sendUDP.py abc  33001  127.0.0.1")
    sys.exit(0)
    
if len(sys.argv)<3:
    usage()

DATA=sys.argv[1]
HOST="127.0.0.1"
if len(sys.argv)>=3:
    PORT=sys.argv[2]
if len(sys.argv)>=4:
    HOST=sys.argv[3]


    
#
# connect to UDP broadcast port for sending commands
#
s = socket(AF_INET, SOCK_DGRAM)
#s.bind(('192.168.1.255', 0))
#s.bind((HOST, MYPORT))
s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

if DATA=='bintest':
    from struct import *
    b=''
    for i in range(47):
        b+=pack('d',float(i))
    s.sendto(b, (HOST, int(PORT)))
    
else:
    s.sendto(DATA.encode(), (HOST, int(PORT)))

