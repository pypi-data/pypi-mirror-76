#! /usr/bin/env python3
'''
Ping package

Usage (from shell):
    $ python -m ping

API:
    from ping import Ping

    ping_once = Ping('localhost')
    print(ping_once.avg)
    print(ping_once.avg)

    ping_more = Ping()
    ping_more.ping('localhost')
    print(ping_more.avg)
    ping_more.ping('google.com')
    print(ping_more.avg)
'''

import os
from subprocess import run
import re


class Ping:
    '''The class Ping'''
    def __init__(self, host=None, count=3) -> None:
        '''Initiate the class Ping'''
        if host: self.ping(host, count)
    def ping(self, host, count=3) -> None:
        '''
        Run ping

        Arguments:
            host (str): Hostname or IP address to be pinged
            count (int, optional): Number of pings to run (default: 3)

        Attributes:
            returncode (int): error return codes (ideal: 0; if returncode<0, it's an app error)
            stderr (str): OS error message
            min (int): Lowest ping response, in milli-seconds
            avg (int): Average ping response, in milli-seconds
            max (int): Highest ping response, in milli-seconds
        '''
        assert isinstance(count, int), f'count arg is {type(count)}, not int'
        assert len(host) > 0, f'host arg must be a valid hostname or IP'

        self.returncode = None
        self.stderr = None
        self.min = None
        self.avg = None
        self.max = None

        if os.name == 'nt':
            cmd = [ 'ping', '-n', str(count), host ]
            comp = re.compile('.*Minimum = (\d+)ms, Maximum = (\d+)ms, Average = (\d+)ms.*')
            imin, imax, iavg = 0, 1, 2
            # Ping expected stdout: ... Minimum = 69ms, Maximum = 69ms, Average = 69ms

        else:
            cmd = [ 'ping', '-q', '-n', '-c', str(count), host ]
            comp = re.compile('.*min/avg/max/mdev = ([\d\.]+)/([\d\.]+)/([\d\.]+)/[\d\.]+ ms.*')
            imin, iavg, imax = 0, 1, 2
            # Ping expected stdout: ... min/avg/max/mdev = 10.844/10.844/10.844/0.000 ms

        res = run(cmd, capture_output=True)
        self.returncode = res.returncode

        if self.returncode > 0:
            if os.name == 'nt': self.stderr = res.stdout.decode().rstrip('\r\n')
            else: self.stderr = res.stderr.decode().rstrip('\n')
            return None

        if not 'avg' in res.stdout.decode() and not 'Average' in res.stdout.decode():
            self.returncode = -1
            self.stderr = 'no data received from ping'
            return None

        s = comp.findall(res.stdout.decode())
        if not s or not isinstance(s, list):
            self.returncode = -2
            self.stderr = 'no data list parsed from ping'
            return None
        elif not s[0] or not isinstance(s[0], tuple):
            self.returncode = -4
            self.stderr = 'no data tuple parsed from ping'
            return None

        self.min = round(float(s[0][imin]))
        self.avg = round(float(s[0][iavg]))
        self.max = round(float(s[0][imax]))

