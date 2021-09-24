'''
Created on Jul 5, 2021

@author: blew
'''

import sys, time
import os
from socket import *
# sys.path.append(os.environ['OCRA_TOOLKIT_DIR']+'/scripts/fluxCalibration/')  # FOR EXTRA MODULES LOCATED IN LOCAL DIRECTORY
# from pyCPEDScommonFunctions import cpedsPythCommon
import socket
import struct


def getUDPdatagram(ip,port, multicast=False):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#     if multicast:
#         s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32) 
#         s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 1)
    
    s.bind((ip, port))
    if multicast:
        MCAST_GRP=ip
        mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
        s.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    while 1:
        data, addr = s.recvfrom(1500)
#         i+=1
        
        yield data.decode()


def udpsrv(args, **kwargs):
    print("Started srv thread")
    for d in getUDPdatagram(args.srvhost,args.srvport):
        if args.verbose>1:
            print("received new UDP: {}".format(d))
        if 'srv' in kwargs.keys():
            kwargs['srv']['toserial']=d
            if args.verbose>2:
                print('storing to shared buffer')
    print("finishing srv thread")
    return 0
