#!/usr/bin/python
# -*- coding: utf-8 -*-
import socket
import argparse

# python main.py -host google.com -s 80 -e 80
parser = argparse.ArgumentParser(description='Scaner portov')
parser.add_argument('-host', action='store', dest='host', help='Host ip', type=str, default="127.0.0.1", nargs='?')
parser.add_argument('-s', action='store', dest='start', help='Start port', type=int, default=1, nargs='?')
parser.add_argument('-e', action='store', dest='end', help='End port', type=int, default=65535, nargs='?')

args = parser.parse_args()

for port in range(args.start, args.end + 1):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((args.host, port))
    if result == 0:
        print("%s:%i is open" % (args.host, port))
    else:
        print("%s:%i is not open" % (args.host, port))
    sock.close()
