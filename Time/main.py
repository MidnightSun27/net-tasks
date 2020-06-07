#!/usr/bin/python
# -*- coding: utf-8 -*-
import socket
from datetime import datetime

shift = 1000

try:
    with open("conf") as f:
        shift = int(f.readline())
except:
    print("Не удалось прочитать конфиг")

UDP_IP = "127.0.0.1"
UDP_PORT = 12300

sock = socket.socket(socket.AF_INET,  
                     socket.SOCK_DGRAM)  
sock.bind((UDP_IP, UDP_PORT))

while True:
    print("listening message")
    data, addr = sock.recvfrom(1024)  
    print("received message: %s" % data)
    time = int((datetime.utcnow() - datetime(1970, 1, 1)).total_seconds())
    tochnoeVremya = str(time + shift).encode()
    print("Sending tochnoe vremya")
    sock.sendto(tochnoeVremya, addr)
