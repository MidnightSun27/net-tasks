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
# Проверять в терминале через команду `nc 127.0.0.1 12300 -u` и жмешь enter, чтобы он отправил UDP пакет

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

while True:
    print("listening message")
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    print("received message: %s" % data)
    time = int((datetime.utcnow() - datetime(1970, 1, 1)).total_seconds())
    tochnoeVremya = str(time + shift)
    print("Sending tochnoe vremya")
    sock.sendto(tochnoeVremya, addr)