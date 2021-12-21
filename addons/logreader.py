import os
from sys import exit
from glob import glob
from time import ctime

os.chdir("../")
dirs = os.listdir(os.getcwd())
if "daemon" in dirs:
    try:
        os.chdir("./daemon/logs")
    except FileNotFoundError:
        print("Directory \"daemon\" doesn't contain a \"logs\" directory")
        sys.exit(0)
else:
    print("Directory \"daemon\" not found, using development path")
    try:
        os.chdir("/home/elias/dev/ground-assistant/daemon/logs")
    except FileNotFoundError:
        print("Directory \"daemon\" not found.")
        sys.exit(0)


logfiles = glob(os.getcwd() + "/*.log")
logs = {}
date = "Oct 29" #ctime()[4:-14]

for item in logfiles:
    file = open(item, "r")
    data = file.read().split("\n")
    file.close()

    content = []
    for line in data:
        if date in line:
            content.append(line[7:])

    logs[item[item.rfind("/") + 1:-4]] = content

aprs_error = []

keyerror = []
foundkeys = []
supposedkeys = []

#print(logs.keys())
for key in logs:
    if key == "aprs_error":
        for line in logs[key]:
            aprs_error.append(line[10:])

    #elif key == "keyerror":
    #    #print(logs[key])
    #    for line in logs[key]:
    #        foundkeys = []
    #        line = line[11:]

    #        while line.find("': ") != -1:
    #            end = line.find("': ")
    #            tmp = line[:end]
    #            start = tmp.rfind("'")
    #            foundkeys.append(tmp[start + 1:])
    #            line = line[end + 3:]
    #
    #        abgleich foundkeys / supposedkeys, fehlende werden ausgegeben


