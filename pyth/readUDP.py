#!/usr/bin/env python3
import sys, time
import os
from socket import *
# sys.path.append(os.environ['OCRA_TOOLKIT_DIR']+'/scripts/fluxCalibration/')  # FOR EXTRA MODULES LOCATED IN LOCAL DIRECTORY
# from pyCPEDScommonFunctions import cpedsPythCommon
import socket
import struct


def getUDPdatagram(ip,port,N, multicast=False):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#     if multicast:
#         s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32) 
#         s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 1)
    
    s.bind((ip, port))
    if multicast:
#         print "subscribing to multicast"
        MCAST_GRP=ip
#         host = socket.gethostbyname(socket.gethostname())
        mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
        s.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
#         s.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_IF, socket.inet_aton(host))
#         s.setsockopt(socket.SOL_IP, socket.IP_ADD_MEMBERSHIP, socket.inet_aton(MCAST_GRP) + socket.inet_aton(host))
    print(("waiting on port:", port))
    i=0
    allData=list()
    while 1:
        data, addr = s.recvfrom(1500)
        allData.append(data)
        i+=1
        if i==N:
            return allData



# print(len(sys.argv))

if len(sys.argv)==1:
    print("USAGE: readUDP.py [port [interface=0.0.0.0 [multicast=1/0]]]")
    print('''Example: read non-multicast datagrams on port 33001 at localhost: 
    
(venv) $ readUDP 33001 127.0.0.1 0

''')
    sys.exit(0)

PORT=33001
HOST='0.0.0.0'
isMULTICAST=False 
if len(sys.argv)>1:
    PORT=sys.argv[1]
if len(sys.argv)>2:
    HOST=sys.argv[2]

if len(sys.argv)>3:
    multi=sys.argv[3]
    if multi=='1':
        isMULTICAST=True

print('listening to port: ',PORT)
print('interface: ',HOST)
print('multicast: ',isMULTICAST)

while 1:
    bindata=getUDPdatagram(HOST, int(PORT), 1, isMULTICAST)

    print(bindata,len(bindata[0]),'chars ',len(bindata[0].split()),' words')
    
