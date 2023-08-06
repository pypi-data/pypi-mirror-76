#! /usr/bin/env python3
'''
Ping package execution

Usage (from shell):
    $ python -m ping
'''

from . import Ping


if __name__ == '__main__':
    host = input('Inform hostname or IP: ')

    if len(host) != 0:
        ping = Ping(host)

        if ping.returncode != 0:
            print(f'Ping returns error: {ping.stderr!r}')
        else:
            print(f'Ping avg return: {ping.avg} ms')

