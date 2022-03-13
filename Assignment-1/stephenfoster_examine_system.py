# Auth: Stephen Foster CS-446, Feb '22

# stephenfoster_examine_system.py

# Prints the following:

# CPU type and model.
# Kernel version details. 
# Amount of time since last boot.
# The time that the system was last booted (same format)- Note: this is not the same as 3, try exploring the systemd process.
# The number of disk requests made. 
# The number of processes created since last boot.

# To: <netid>_systemDetails.txt

import os
import datetime
from sys import platform

def main():

    if platform != "linux":
        print("Oops! You're running this script from " + platform.capitalize() + "!")
        exit()
    
    netid = "stephenfoster"
    self = netid + "_examine_system.py"
    out_file = netid + "_systemDetails.txt"
    out_path = os.path.split(os.path.join(os.getcwd(), self))[0]

    #Take and parse input from /proc
    cpuinfo        = parseForStart(getRaw("/proc/cpuinfo"), ["model name", "cpu cores"])
    version        = fixListToStr(getRaw("/proc/version"))
    uptime         = float(parsePos(fixListToStr(getRaw("/proc/uptime")), 0, " "))
    systemd        = int(parsePos(fixListToStr(getRaw("/proc/1/stat")), 21, " "))
    boottime       = int(parsePos(fixListToStr(parseForStart(getRaw("/proc/stat"), ["btime"])), 1, " "))
    diskstats      = parsePos(fixListToStr(parseForRelSub(getRaw("/proc/diskstats"), ["sda1"], -1)), 1, "sda")
    vmstats        = parseForStart(getRaw("/proc/vmstat"), ["pgpgin", "pgpgout", "pswpin", "pswpout"])
    processes      = parsePos(fixListToStr(parseForStart(getRaw("/proc/stat"), ["processes"])), 1, " ")

    #Format uptime from /proc/uptime
    uptime = str(datetime.timedelta(seconds=int(uptime)))

    #Calculate boot date/time from /proc/1/stat starttime(22) [boot time since epoch + time elapsed until systemd = start date]
    HZ = os.sysconf(os.sysconf_names['SC_CLK_TCK'])
    boottime += systemd/HZ
    boottime = str(datetime.datetime.fromtimestamp(int(boottime)))
    
    #Further parse and fill diskstats
    reads = "Reads: " + parsePos(diskstats, 1, " ")
    writes = "Writes: " + parsePos(diskstats, 5, " ") + "\n"
    diskstats = [reads, writes]
    
    #Output polishing
    cpuinfo.insert(0, "(1) CPU Type and Model:\n")
    for x in range(1, len(cpuinfo)):
        cpuinfo[x] = "\t" + cpuinfo[x]
    version = ("(2) Kernel Version:\n\t") + version
    uptime = "(3) Uptime: " + str(uptime)
    boottime = "(4) System Boot: " + boottime
    diskstats = ["(5) Disk Requests:\n"] + diskstats
    for x in range(1, len(diskstats)):
        diskstats[x] = "\t" + diskstats[x]
    processes = "(6) Processes: " + fixListToStr(processes)

    #Fill an output buffer and write it to the out file
    buffer = [cpuinfo, version, uptime, boottime, diskstats, processes]
    clearFile(out_path, out_file)

    for item in buffer:
        if type(item) == list:
            for s in item:
                outputToFile(out_path, out_file, str(s))
        elif type(item) == str:
            outputToFile(out_path, out_file, item + "\n")
        else:
            outputToFile(out_path, out_file, str(item))

def getRaw(_path):
    fin = open(_path, "r")
    raw = fin.readlines()
    fin.close()
    return raw

def parseForRelSub(_lines, _strs, _pos):
    hits = []
    numLines = 0
    for line in _lines:
        for _str in _strs:
            if _str in line:
                hits = hits[:] + [_lines[numLines + _pos]]
        if len(hits) == len(_strs):
            return hits
        numLines += 1
    return hits

def parseForSub(_lines, _strs):
    hits = []
    for line in _lines:
        for _str in _strs:
            if line.find(_str):
                hits = hits[:] + [line]
        if len(hits) == len(_strs):
            return hits
    return hits

def parseForStart(_lines, _strs):
    hits = []
    for line in _lines:
        for _str in _strs:
            if line.startswith(_str):
                hits = hits[:] + [line]
        if len(hits) == len(_strs):
            return hits
    return hits
            
def parsePos(_line, _pos, _delin):
    positions = _line.split(_delin)
    return positions[_pos]

def fixListToStr(_list):
    return str(_list).replace('[','').replace(']','').replace('\'', '').replace('\\n', '')

def outputToFile(_path, _out_file, _str):
    fout = open(_path + "/" + _out_file, "a")
    fout.write(_str)
    fout.close()

def clearFile(_path, _out_file):
    fout = open(_path + "/" + _out_file, "w")
    fout.write('')
    fout.close()

if __name__ == '__main__':
    main()