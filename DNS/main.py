#!/usr/bin/python
# -*- coding: utf-8 -*-

from dnslib import DNSRecord
import socket
import pickle

FORWARDED_ADDRESS = ("8.8.8.8", 53)
SERVER_ADDRESS = ("127.0.0.1", 53)


class Record:
    def __init__(self, name, req_type, data):
        self.name = name
        self.req_type = req_type
        self.data = data


def save_cache():
    with open("cache", "wb") as file:
        pickle.dump(CACHE, file)


def open_cache():
    try:
        with open("cache", "rb") as file:
            return pickle.load(file)
    except FileNotFoundError:
        temp = []
        with open("cache", "wb") as file:
            pickle.dump(temp, file)
        return temp


CACHE = open_cache()


def packet_parse(name, packet):
    pack = DNSRecord.parse(packet)
    for ar in pack.ar:
        for record in CACHE:
            if record.name != name and record.req_type != ar.rtype:
                add_to_cache(name, ar.rtype, packet)

    for auth in pack.auth:
        for record in CACHE:
            if record.name != name and record.req_type != auth.rtype:
                add_to_cache(name, auth.rtype, packet)


def add_to_cache(address, request_type, response):
    record = Record(address, request_type, response)
    CACHE.append(record)


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(SERVER_ADDRESS)
    while True:
        data, addr = sock.recvfrom(1024)
        print(data, addr)
        header = data[:12]
        req_id = header[:2]
        length = data[12]
        current_index = 12
        address = ""
        while length != 0:
            l = length
            name = data[current_index + 1: current_index + 1 + length].decode()
            address += name + "."
            current_index += l + 1
            length = data[current_index]
        request_type = data[current_index + 2]
        in_cache = False
        for rec in CACHE:
            if rec.name == address and rec.req_type == request_type:
                in_cache = True
                answer = req_id + rec.data[2:current_index + 2] + \
                         request_type.to_bytes(1, "big") + \
                         rec.data[current_index + 3:]
                sock.sendto(answer, addr)
                break
        if in_cache:
            save_cache()
            print("from cache")
            continue
        print("from forwarder")
        forwarded_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        forwarded_socket.settimeout(2)
        forwarded_socket.sendto(data, FORWARDED_ADDRESS)
        response = forwarded_socket.recvfrom(1024)
        forwarded_socket.close()
        answer = response[0]
        sock.sendto(answer, addr)
        add_to_cache(address, request_type, answer)
        packet_parse(address, answer)


if __name__ == '__main__':
    main()
