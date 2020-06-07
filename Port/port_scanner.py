import socket
import sys


def port_scanner(left, right, _ip='localhost'):
    for port in range(left, right):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        with sock:
            if not sock.connect_ex((_ip, port)):
                print(f'Port {port} is open')
            else:
                print(f'Port {port} is close')


def main():
    lo, hi = 0, 65_535
    left, right = tuple(map(int, sys.argv[1:]))
    if lo <= left and right <= hi:
        port_scanner(left, right)
    else:
        print(f'Range [{left}, {right}] is incorrect.')


if __name__ == '__main__':
    main()
