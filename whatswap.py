#!/usr/bin/env python3
import os, re

dst = os.listdir("/proc")
print("{:<10}{:<10}{:<10}".format("PID", "Swap", "Name"))
for l in filter(str.isdigit, dst):
    with open("/proc/"+l+"/status") as f:
        f = f.read()
        s = re.search(r'VmSwap:.*', f)
        n = re.search(r'Name:.*', f)
        if s:
            s = re.split(':', s.group(0))
            n = re.split(':', n.group(0))
            s = s[1].lstrip()
            n = n[1].lstrip()
            if s != '0 kB':
                print("{:<10}{:<10}{:<10}".format(l, s, n))
