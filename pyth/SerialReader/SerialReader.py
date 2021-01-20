'''
Created on Oct 6, 2020

@author: blew
'''
# from random import random


def serialBytesGen(sercon):
    while True:
        b=sercon.read(1)
        yield b.decode()

def serialLineGen(sercon,args):
    while True:

        if args.dummy!="":
            import time
#             print('.',end='',flush=True)
            time.sleep(args.dummy_wait)
            s=args.dummy
        else:
            b=None
            l=[]
            while b!=b'\n':
                b=sercon.read(1)
                l.append(b.decode())
            s=''.join(l)[0:-1]
            s=s[0:-1] if s.endswith('\r') else s
        yield s


        