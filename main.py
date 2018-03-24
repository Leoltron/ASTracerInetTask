# !/usr/bin/env python3

import re
import sys

import ipinfo
from table import print_table
from traceroute import tracert

IP_REGEXP = re.compile(r"([\d]{,3})\.([\d]{,3})\.([\d]{,3})\.([\d]{,3})")


def is_ip(s: str) -> bool:
    match = IP_REGEXP.fullmatch(s)
    return bool(
        match and all(0 <= int(match.groups()[i]) <= 255 for i in range(4)))


def is_white_ip(ip: str) -> bool:
    if not is_ip(ip):
        return False
    parts = [int(s) for s in ip.split('.')]
    return not (parts[0] == 10) and \
           not (parts[0] == 127) and \
           not (parts[0] == 100 and 64 <= parts[1] <= 127) and \
           not (parts[0] == 172 and 16 <= parts[1] <= 31) and \
           not (parts[0] == 192 and parts[1] == 168)


HOSTNAME_REGEXP = re.compile(r"(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)


def is_valid_hostname(hostname: str) -> bool:
    splitted = hostname.split('.')
    if len(splitted[-1]) == 0 and len(splitted) > 1:
        return all(HOSTNAME_REGEXP.fullmatch(s) for s in splitted[:-1])
    return all(HOSTNAME_REGEXP.fullmatch(s) for s in splitted)


def trace_as(host):
    trace_steps = tracert(host)
    cleaned_steps = [(n, ipinfo.IPInfo.from_ip(ip))
                     if is_white_ip(ip)
                     else (n, ipinfo.IPInfo(ip))
                     for n, ip in trace_steps]
    table = [('#', 'IP', 'AS', 'Country', 'Organisation'), ('',) * 5]
    for number, trace_step in cleaned_steps:
        table.append((number, trace_step.ip, trace_step.as_number,
                      trace_step.country_code, trace_step.company))
    print_table(table)


def main():
    trace_as(' '.join(sys.argv[1:]))


if __name__ == '__main__':
    debug = False
    if "-d" in sys.argv:
        sys.argv.remove("-d")
        debug = True
    try:
        main()
    except Exception as e:
        if debug:
            raise
        else:
            print("Error: " + str(e))
