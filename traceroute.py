# !/usr/bin/env python3
import re

import subprocess

TRACE_STEP_REGEXP = re.compile(
    r"\s*(\d+)(?:\s+(?:\d+ ms|\*)){0,3}\s+(\S+(?:\s+\S+)*)\s*")


def tracert(host: str):
    return list(_tracert_gen(host))


def _tracert_gen(host: str):
    print("Tracing route to ["+host+"]...")
    trace_results = subprocess.check_output(["tracert", "-d", host])
    for i in trace_results.split(b'\r\n')[4:-3]:
        fullmatch = TRACE_STEP_REGEXP.fullmatch(i.decode(encoding='cp866'))
        if fullmatch:
            yield fullmatch.groups()
        else:
            print(str(i)+" tracert return string: can't match!")
            print('\tBytes: "' + str(i) + '"')
            print('\tDecoded: "' + i.decode(encoding='cp866') + '"')
