#!/usr/bin/env python
'''
serial2udp -- connect to serial port and dump data to UDP packages

serial2udp is a serial2udp transmitter

It defines classes_and_methods

@author:     Bartosz Lew

@copyright:  2020 Bartosz Lew. All rights reserved.

@license:    GPL

@contact:    bartosz.lew@protonmail.com
@deffield    updated: Updated
'''

import sys
import os
from multiprocessing import Process,Manager

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

from socket import *
import serial

from SerialReader import SerialReader, UDPreader



__all__ = []
__version__ = 0.1
__date__ = '2020-10-06'
__updated__ = '2020-10-06'

DEBUG = 1
TESTRUN = 0
PROFILE = 0

class CLIError(Exception):
    '''Generic exception to raise and log different fatal errors.'''
    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "E: %s" % msg
    def __str__(self):
        return self.msg
    def __unicode__(self):
        return self.msg


def init_serial(args):
    PARITY=serial.PARITY_NONE
    if args.parity=='None':
        PARITY=serial.PARITY_NONE
    else:
        raise 'Unsupported parity'
    TIMEOUT  = 0.05

    ser=None
    if args.dummy=='':
        ser=serial.Serial(port=args.serport, 
                          baudrate=args.baudrate, 
                          parity=PARITY, 
                          bytesize=args.bytesize, 
                          stopbits=args.stopbits, 
                          timeout=TIMEOUT)
    
        if ser.port is None:
            ser.port.open()

    return ser

def dump_serial(args, **kwargs):
    '''
    '''
    ser=init_serial(args)
    
    srvdata=Manager().dict()
    srvdata['toserial']=None
    kwargs['srv']=srvdata

    if args.verbose>1:
        print('starting srv thread')

    p=Process(target=UDPreader.udpsrv,
              args=(args,),
              kwargs=kwargs,
              daemon=True,
              )
    p.start()
#     p.join()
    
    if args.verbose>1:
        print('starting srv thread')
    
    udpsock = socket(AF_INET, SOCK_DGRAM)
    udpsock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    
#     for s in SerialReader.serialLineGen(ser):
    for s in SerialReader.serialLineGen(ser, args):
        send_line=False
        if args.ifstarts_with!='':
            if s.startswith(args.ifstarts_with):
                send_line=True
                s=s[len(args.ifstarts_with):]
        else:
            send_line=True

        if send_line:
#             print('.',end='',flush=True)
            if args.verbose>1:
                print(s)
            count=udpsock.sendto(s.encode(), (args.host, args.port))
        else:
            if args.verbose>1:
                print('line does not match ({})'.format(s))


        if srvdata['toserial']!=None:
            print('sending to serial: "{}"'.format(srvdata['toserial']))
            if not srvdata['toserial'].endswith('\n'):
                srvdata['toserial']=srvdata['toserial']+'\n'
            ser.write(srvdata['toserial'].encode())
            srvdata['toserial']=None
            

def read_test(args):
    ser=init_serial(args)
    while 1:
#         s=input('input character to send: ')
        s='DUPA\n'
        print('sending "{}" to serial'.format(s))
        ser.write(s.encode())
        b=None
        msg=''
        while b!=b'\n':
            b=ser.read(1)
            msg=msg+b.decode()
        print('received: "{}"'.format(msg))
            
            
                
def main(argv=None): # IGNORE:C0111
    '''Command line options.'''

    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_name = os.path.basename(sys.argv[0])
    program_version = "v%s" % __version__
    program_build_date = str(__updated__)
    program_version_message = '%%(prog)s %s (%s)' % (program_version, program_build_date)
    program_shortdesc = __import__('__main__').__doc__.split("\n")[1] if __import__('__main__').__doc__ !=None else ''
    program_epilog ='''
    
Examples:

serial2udp.py --serport /dev/device1 --host xxx.xxx.xxx.xxx -p port --ifstarts_with 'udp '
 
'''
    program_license = '''%s

  Created by Bartosz Lew on %s.
  Copyright 2020 Bartosz Lew. All rights reserved.

  Licensed under the Apache License 2.0
  http://www.apache.org/licenses/LICENSE-2.0

  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

USAGE
''' % (program_shortdesc, str(__date__))

    try:
        # Setup argument parser
        parser = ArgumentParser(description=program_license, epilog=program_epilog, formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument("-v", "--verbose", dest="verbose", action="count", help="set verbosity level [default: %(default)s]", default=0)
        parser.add_argument('-V', '--version', action='version', version=program_version_message)

        parser.add_argument('--serport', type=str, help='serial port [default: %(default)s] ', default='/dev/ttyACM1')
        parser.add_argument('--baudrate', type=int, help='serial communication baudrate [default: %(default)s] ', default=9600)
        parser.add_argument('--parity', type=str, help='serial communication parity [default: %(default)s] ', default='None')
        parser.add_argument('--bytesize', type=int, help='serial communication bytesize [default: %(default)s] ', default=8)
        parser.add_argument('--stopbits', type=int, help='serial communication stopbits [default: %(default)s] ', default=1)
        parser.add_argument('--host', type=str, help='UDP datagram destination host [default: %(default)s] ', default='127.0.0.1')
        parser.add_argument('--srvhost', type=str, help='UDP to serial command server address [default: %(default)s] ', default='127.0.0.1')
        parser.add_argument('--srvport', type=int, help='UDP to serial command server port [default: %(default)s] ', default=10001)
        parser.add_argument('-p','--port', type=int, help='UDP destination port [default: %(default)s] ', default=10000)
        parser.add_argument('--dummy', type=str, 
                            help='String that should be sent. No serial port is read. [default: %(default)s] ', default='')
        parser.add_argument('--dummy_wait', type=int, 
                            help='Wait time [s] between two dummy sends. [default: %(default)s] ', default=1)
        parser.add_argument('--ifstarts_with', type=str, 
                            help='send UDP only if the serial line starts with this string [default: %(default)s] ', default='')
        
        parser.add_argument('--read_test',action='store_true', default=False, help='triggers read send read mode')

        # Process arguments
        args = parser.parse_args()

        verbose = args.verbose

        if verbose > 1:
            print("Verbose mode on ({})".format(args.verbose))


        if args.read_test:
            read_test(args)
            sys.exit(0)
        
        dump_serial(args)

        return 0
    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 0
    except Exception as e:
        if DEBUG or TESTRUN:
            raise(e)
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        return 2

if __name__ == "__main__":
    if DEBUG:
        sys.argv.append("-v")
    if TESTRUN:
        import doctest
        doctest.testmod()
    if PROFILE:
        import cProfile
        import pstats
        profile_filename = 'serial2udp_profile.txt'
        cProfile.run('main()', profile_filename)
        statsfile = open("profile_stats.txt", "wb")
        p = pstats.Stats(profile_filename, stream=statsfile)
        stats = p.strip_dirs().sort_stats('cumulative')
        stats.print_stats()
        statsfile.close()
        sys.exit(0)
    sys.exit(main())