# Import cool new rpc module that gives us more control and gets rid of headaches :)
from pypresence import Presence
import time
import sys
import os
# import info about system
from fetch_cord.args import parse_args
from fetch_cord.testing import uptime, gpuid, desktopid, appid, cpuappid, termappid
from fetch_cord.out import cpuline, packagesline, termid, shellid, kernelline, gpuinfo, shell_line, termfontline, \
    sysosline, sysosid, dewmid

args = parse_args()


def main():
    # printing info with debug switch
    if args.debug:
        print("run-rpc")
        print(uptime)
        print(packagesline[0])
        print(appid)
        print(gpuid)
    if sysosid.lower() == "macos":
        runmac()
    elif sysosid.lower() in ["windows10", "windows7", "windows8.1", "windows8"]:
        wandowz()
    else:
        loonix()


print("Connecting")
time.sleep(5)
# discord uses unix time to interpret time for rich presnse, this is uptime in unix time
start_time = float(uptime)
print("RPC connection successful.")


def runmac():
    from fetch_cord.testing import devicetype, product, bigicon, ver
    client_id = '740822755376758944'  # macos appid for discord rpc
    time.sleep(5)
    start_time = float(uptime[:-1])
    while True:
        RPC = Presence(client_id)
        RPC.connect()
        RPC.update(state=packagesline[0],  # uptadte state as packages
                   details=kernelline[0],  # update details as kernel
                   large_image=bigicon,  # set icon
                   large_text=sysosline[0],  # set large icon text
                   small_image=devicetype,  # set small image icon
                   small_text=product,  # set small image text
                   start=start_time)
        time.sleep(30)


def custom_time():
    ctime = int(args.time)
    time.sleep(ctime)


# cycle


def cycle0():
    global RPC
    if args.debug:
        print("cycle 0")
    client_id = appid
    RPC = Presence(client_id)
    RPC.connect()
    RPC.update(state=packagesline[0],
               details=kernelline[0],
               large_image="big",
               large_text=sysosline[0],
               small_image=desktopid,
               small_text=dewmid,
               start=start_time)
    if args.debug:
        print("appid: %s" % client_id)

    if args.time:
        custom_time()
    elif args.distro and not args.shell and not args.hardware:
        time.sleep(9999)
    else:
        time.sleep(30)


# cycle


def cycle1():
    global RPC
    if args.debug:
        print("cycle 1")
    client_id = cpuappid
    RPC = Presence(client_id)
    RPC.connect()
    RPC.update(state=cpuline[0],
               details=gpuinfo,
               large_image="big",
               large_text=cpuline[0],
               small_image=gpuid,
               small_text=gpuinfo,
               start=start_time)
    if args.debug:
        print("appid: %s" % client_id)
    if args.time:
        custom_time()
    elif args.hardware and not args.distro and not args.shell:
        time.sleep(9999)
    else:
        time.sleep(30)


# cycle


def cycle2():
    global RPC
    if args.debug:
        print("cycle 2")
    client_id = termappid
    RPC = Presence(client_id)
    RPC.connect()
    RPC.update(state=shell_line[0],
               details=termfontline[0],
               large_image="big",
               large_text=termid,
               small_image=shellid,
               small_text=shellid,
               start=start_time)
    if args.debug:
        print("appid: %s" % client_id)
    if args.time:
        custom_time()
    elif args.shell and not args.distro and not args.hardware:
        time.sleep(9999)
    else:
        time.sleep(30)


def w_cycle0():
    global RPC
    if args.debug:
        print("cycle 2")
    client_id = termappid
    RPC = Presence(client_id)
    RPC.connect()
    RPC.update(state=sysosline[0],
               details=memline[0],
               large_image="big",
               large_text=sysosline[0],
               small_image=moboid,
               small_text=moboline[0],
               start=start_time)
    if args.debug:
        print("appid: %s" % client_id)
    if args.time:
        custom_time()
    elif args.shell and not args.distro and not args.hardware:
        time.sleep(9999)
    else:
        time.sleep(30)


def w_cycle1():
    global RPC
    if args.debug:
        print("cycle 2")
    client_id = termappid
    RPC = Presence(client_id)
    RPC.connect()
    RPC.update(state=cpuline[0],
               details=gpuinfo,
               large_image="big",
               large_text=cpuline[0],
               small_image=gpuid,
               small_text=gpuinfo,
               start=start_time)
    if args.debug:
        print("appid: %s" % client_id)
    if args.time:
        custom_time()
    elif args.shell and not args.distro and not args.hardware:
        time.sleep(9999)
    else:
        time.sleep(30)



def loonix():
    try:
        while True:
            if args.distro and not args.shell and not args.hardware:
                cycle0()
            elif args.hardware and not args.distro and not args.shell:
                cycle1()
            elif args.shell and not args.distro and not args.hardware:
                cycle2()
            elif args.distro and args.hardware and not args.shell:
                cycle0()
                RPC.clear(pid=os.getpid())
                cycle1()
                RPC.clear(pid=os.getpid())
            elif args.distro and args.shell and not args.hardware:
                cycle0()
                RPC.clear(pid=os.getpid())
                cycle2()
                RPC.clear(pid=os.getpid())
            elif args.hardware and args.shell and not args.distro:
                cycle1()
                RPC.clear(pid=os.getpid())
                cycle2()
                RPC.clear(pid=os.getpid())
            else:
                cycle0()
                RPC.clear(pid=os.getpid())
                cycle1()
                RPC.clear(pid=os.getpid())
                cycle2()
                RPC.clear(pid=os.getpid())
    except KeyboardInterrupt:
        print("Closing connection.")
        sys.exit(0)


def wandowz():
    try:
        while True:
            if args.distro not in [args.hardware]:
                w_cycle0()
            elif args.hardware not in [args.distro]:
                w_cycle1()
            else:
                w_cycle0()
                RPC.clear(pid=os.getpid())
                w_cycle1()
                RPC.clear(pid=os.getpid())
    except KeyboardInterrupt:
        print("Closing connection.")
        sys.exit(0)
