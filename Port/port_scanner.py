import asyncio
import sys


async def checker(port, _ip='localhost'):
    try:
        reader, writer = await asyncio.co(_ip, port)

        print(f'Port {port} is open')
        writer.close()
    except Exception:
        print(f'Port {port} is close')


async def port_scanner(left, right):
    for port in range(left, right + 1):
        await checker(port)


def main():
    lo, hi = 0, 65_535
    left, right = tuple(map(int, sys.argv[1:]))
    if lo <= left and right <= hi:
        loop = asyncio.get_event_loop()
        tasks = [loop.create_task(checker(border_port)) for border_port in range(left, right)]
        loop.run_until_complete(asyncio.wait(tasks))
    else:
        print(f'Range [{left}, {right}] is incorrect.')


if __name__ == '__main__':
    main()
