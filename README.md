#GENERAL

This package implements serial port to UDP packet transceiver.

#DOWNLOAD 

`git clone ssh://gitolite@galaxy.astro.uni.torun.pl/rt32tmsrv`

#INSTALL FROM SOURCE

	$ git clone ssh://gitolite@galaxy/serial2udp serial2udp
	$ cd serial2udp
	$ python3 -m venv venv
	$ source venv/bin/activate
	$ python setup.py build
	$ python setup.py install

#USE

Suppose you read data from a serial port of a device /dev/device1 and want to distribute that data via UDP packages to a local network

Suppose the device generates ascii text lines:

	line1 word1 word2 ...
	line2 word3 word4 ...
	...
	udp key1=val1, key2=val2,...
	lineN ...
	udp key3=val3, key4=val4,...


If we wish to distribute lines only that start with udp run:

	serial2udp.py --serport /dev/device1 --host xxx.xxx.xxx.xxx -p port --ifstarts_with 'udp'

For the example above this command will generate two UDP datagrams.

The program does not parse the data in any way, but if --ifstarts_with option is used, the line string is stripped with the value of that option ("udp" in this case).

The serial communication options are customizable.

#HELP

	$ path/to/serial2udp/venv/bin/serial2udp.py --help

	usage: serial2udp.py [-h] [-v] [-V] [--serport SERPORT] [--baudrate BAUDRATE]
                     [--parity PARITY] [--bytesize BYTESIZE]
                     [--stopbits STOPBITS] [--host HOST] [-p PORT]
                     [--dummy DUMMY] [--dummy_wait DUMMY_WAIT]
                     [--ifstarts_with IFSTARTS_WITH]

	serial2udp -- connect to serial port and dump data to UDP packages

	  Created by Bartosz Lew on 2020-10-06.
	  Copyright 2020 Bartosz Lew. All rights reserved.

	  Licensed under the Apache License 2.0
	  http://www.apache.org/licenses/LICENSE-2.0

	  Distributed on an "AS IS" basis without warranties
	  or conditions of any kind, either express or implied.

	USAGE
	
	optional arguments:
	  -h, --help            show this help message and exit
	  -v, --verbose         set verbosity level [default: 0]
	  -V, --version         show program's version number and exit
	  --serport SERPORT     serial port [default: /dev/ttyACM1]
	  --baudrate BAUDRATE   serial communication baudrate [default: 9600]
	  --parity PARITY       serial communication parity [default: None]
	  --bytesize BYTESIZE   serial communication bytesize [default: 8]
	  --stopbits STOPBITS   serial communication stopbits [default: 1]
	  --host HOST           UDP datagram destination host [default: 127.0.0.1]
	  -p PORT, --port PORT  UDP destination port [default: 10000]
	  --dummy DUMMY         String that should be sent. No serial port is read.
	                        [default: ]
	  --dummy_wait DUMMY_WAIT
	                        Wait time [s] between two dummy sends. [default: 1]
	  --ifstarts_with IFSTARTS_WITH
	                        send UDP only if the serial line starts with this
	                        string [default: ]

   


#AUTHOR
Bartosz Lew [<bartosz.lew@umk.pl>](bartosz.lew@umk.pl)

#BUGS
Send info to author or to [rt4-dev@cosmo.torun.pl](rt4-dev@cosmo.torun.pl)
