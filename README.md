# General

This is serial port to UDP packet transceiver.
Read serial port as ascii and send the text as UDP datagrams 
if the lines match given selection criteria, or communicate with
the device via commands provided via UDP datagrams.


# Installation

To install from pypi run

```sh
pip install serial2udp
```

## From Sources

```sh 
git clone https://github.com/bslew/serial2udp.git serial2udp
cd serial2udp
python3 -m venv venv
source venv/bin/activate
python setup.py build install
```

# Use examples
## Example 1

Suppose you read data from a serial port of a device `/dev/device1` and want to distribute that data via UDP packages to a local network.

Suppose the device generates ascii text lines:

	line1 word1 word2 ...

	line2 word3 word4 ...

	 ...

	udp key1=val1, key2=val2, ...

	lineN  ...

	udp key3=val3, key4=val4, ...


If we wish to distribute via UDP only the lines that start with "udp " 
execute:

```sh
(venv) $ serial2udp.py --serport /dev/device1 --host xxx.xxx.xxx.xxx -p port --ifstarts_with 'udp '
```

or simply 

```sh
(venv) $ serial2udp --serport /dev/device1 --host xxx.xxx.xxx.xxx -p port --ifstarts_with 'udp '
```

For the example above, this command will generate two UDP datagrams containing

```
key1=val1, key2=val2, ...
```

and

```
key3=val3, key4=val4, ...
```

The program does not parse the data in any way, but if `--ifstarts_with` option is used, the line string is stripped off of the value given in that option (\'udp \' in this case). The serial communication options are customizable.

## Example 2

Suppose that you want to perform both read and distribute values read from a device and 
also receive simple commands via UDP and send them to the device, for example to change 
state of some relay. Extending the example 1 let's distribute the serialized dictionary
and listen for incomming commands on port 10001 on localhost.
Execute:

```sh
(venv) $ serial2udp.py --serport /dev/device1 --host xxx.xxx.xxx.xxx -p port --ifstarts_with 'udp ' --srvport 10001 --srvhost 127.0.0.1
```

Now if you send UDP datagram to 127.0.0.1:10001 it will be written directly to the serial port.



# Usage


```{r}
$ serial2udp.py --help
usage: serial2udp [-h] [-v] [-V] [--serport SERPORT]
                  [--baudrate BAUDRATE] [--parity PARITY]
                  [--bytesize BYTESIZE] [--stopbits STOPBITS]
                  [--host HOST] [--srvport SRVPORT] [-p PORT]
                  [--dummy DUMMY] [--dummy_wait DUMMY_WAIT]
                  [--ifstarts_with IFSTARTS_WITH] [--read_test]

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
  --srvhost SRVHOST     UDP to serial command server address [default: 127.0.0.1]
  --srvport SRVPORT     UDP to serial command server port [default: 10001]
  -p PORT, --port PORT  UDP destination port [default: 10000]
  --dummy DUMMY         String that should be sent. No serial port is read. [default: ]
  --dummy_wait DUMMY_WAIT
                        Wait time [s] between two dummy sends. [default: 1]
  --ifstarts_with IFSTARTS_WITH
                        send UDP only if the serial line starts with this string [default: ]
  --read_test           triggers read send read mode

    
```


# Additional scripts
## Simple UDP reader

The package contains a simple UDP datagram reader and writer. The read UDP datagrams distributed 
by the serial2udp program use:

```sh
(venv) $ readUDP.py 10001 127.0.0.1 0
```

## Simple UDP writer

In order to send a test UDP datagram use:

```sh
(venv) $ sendUDP.py "example datagram body" 10001 
```


# Author

Bartosz Lew \<bartosz.lew@protonmail.com\>

