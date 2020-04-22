#!/usr/bin/python
# -*- coding: utf-8 -*-

import subprocess
import re
import ipinfo
import sys


access_token = "025d959c10ca78"
handler = ipinfo.getHandler(access_token)

regexp = re.compile(r'((?:[0-9]{1,3}\.){3}[0-9]{1,3})')

cmd_script = 'traceroute'
start_index = 0
if sys.platform == 'win32':
    cmd_script = 'tracert'
    start_index = 2


def get_info_about_ip(ip):
    try:
        info = handler.getDetails(ip)
    except:
        return "Нет информации"
    return "AS : {}, Country: {}".format(info.all.get("org"), info.all.get("country_name"))


def trace_route(url):
    try:
        trace_result = subprocess.check_output([cmd_script, url]).decode("cp866")
        return trace_result
    except subprocess.CalledProcessError:
        return "Что-то пошло не так"


def parse_ip(trace):
    ip = regexp.search(trace)
    return ip


def get_help():
    print("Этот скрипт показывет маршрут от этого компьютера до указанного IP- или URL- адреса")
    print("Инструкции:")
    print("\tpython traceroute.py -h | python traceroute.py --help - показ этого сообщения ")
    print("\tpython traceroute.py <url>")
    print("\tpython traceroute.py yandex.ru")
    print("\tpython traceroute.py <IP>")
    print("\tpython traceroute.py 77.88.55.55")


def main():
    if len(sys.argv) == 1:
        get_help()
        return
    if sys.argv[1] == "-h" or sys.argv[1] == "--help":
        get_help()
        return
    adress = sys.argv[1]
    print("В процессе...")
    trace = trace_route(adress).split('\n')[start_index:]
    index = 1
    for line in trace:
        ip = parse_ip(line)
        if ip is not None:
            ip_info = ip.group(0)
            print(str(index) + ". " + ip_info + " | " + get_info_about_ip(ip_info))
            index += 1


if __name__ == '__main__':
    main()
