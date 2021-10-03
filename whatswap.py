#!/usr/bin/env python3
import os, re, operator, argparse


parser=argparse.ArgumentParser(argument_default='-h', 
                    description='View what processes in swap', usage='whatswap.py -[h|p|s|n]')
parser.add_argument('-p', '--pid', help='sorts output by PID',  
                    metavar='', const='pid', action='store_const')
parser.add_argument('-s', '--swap', help='sorts output by swap size', 
                    metavar='', const='swap', action='store_const')
parser.add_argument('-n', '--name', help='sorts output by swap name', 
                    metavar='', const='name', action='store_const')

arg = parser.parse_args()

allswap = []
dst = os.listdir("/proc")

for pproc in filter(str.isdigit, dst):
    with open("/proc/"+pproc+"/status") as f:
        f = f.read()
        ssize = re.search(r'VmSwap:.*', f)
        nname = re.search(r'Name:.*', f)
        if ssize:
            ssize = re.split(':', ssize.group(0))
            nname = re.split(':', nname.group(0))
            ssize = ssize[1].lstrip().split()
            ssize = int(ssize[0])
            nname = nname[1].lstrip()
            if ssize != 0:
                #print("{:<10}{:<10}{:<10}".format(l, s, n))
                allswap.extend([[int(pproc), ssize, nname]])

def sort_out(s=0, reverse=False):
    listed = sorted(allswap, key=operator.itemgetter(s), reverse=reverse)
    #listed = allswap.sort(key=elem_sort)
    return(listed)

if arg.pid == 'pid':
    listed = sort_out(0)
    #print(listed)
if arg.swap == 'swap':
    listed = sort_out(1, True)
if arg.name == 'name':
    listed = sort_out(2)
try: 
    listed
    print("{:<10}{:<10}{:<10}".format("PID", "Swap", "Name"))
    for process in listed:
        print("{:<10}{:<10}{:<10}".format(process[0], str(process[1])+" kB", process[2]))
    #print(process)
except NameError:
    print("Please use -h key for help")
