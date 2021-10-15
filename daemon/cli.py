#Get sys.argv
import sys
if len(sys.argv) > 4:
    print("Too many arguments. Type \"ground-assistant --help\" to get help.")
    sys.exit()
elif len(sys.argv) < 2:
    print("No action specified. Type \"ground-assistant --help\" to get help.")
    sys.exit()

argument = sys.argv[1]

if argument[0:2] != "--":
    print("Invalid argument. Type \"ground-assistant --help\" to get help.")
    sys.exit()
else:
    argument = argument[2:]

#Get path and config object   #!!! dev is not standart yet
from os import path
devpath = "/home/elias/dev/ground-assistant/daemon"

if argument == "restart":
   position = 3
else:
    position = 2

try:
    upath = sys.argv[position]
    if upath == "--":
        path = devpath
    else:
        upath = upath[2:]
        if upath == "local":
            from os import path
            path = path.abspath(".")
        else:
            path = upath
except:
    path = devpath

try:
    from ground_assistant.load import ReadConfig
    c = ReadConfig(path)
except:
    print("Incorrect path")
    sys.exit(1)
#Functions:
def start(path):
    import os
    os.system("python " + path + "/ground-assistant.py " + path + " &")
    return "Started Ground-Assistant."

def help():
    return """  usage: ground-assistant [--action] [--parameter] [--path]
  ---------------------- actions -----------------------
  --start        start the daemon
  --stop         temporarily stops the data input
  --continue     continue data input after stop
  --close        stop ground-assistant daemon
  --restart      restart ground-assistant daemon
      --direct       sends a restart beacon
      --fully        stops and starts the daemon again
  --status       send status request
  --show         show 10 beacons from data input
  --refresh_ndb  refreshes NameDB
  --help         show this help

  [--path]       --local: use the path the script is
                          started from
                 --/pathtodir/dir: use the given path"""


if argument == "help":
    print(help())

elif argument == "start":
    print(start(path))

elif argument == "restart":
    try:
        mode = sys.argv[2]
        if mode == "--direct":
            mode = "direct"
        else:
            raise Exception()
    except:
        mode = "fully"

    from multiprocessing.connection import Client
    p = c.getconfig("ci")
    address = ('localhost', p["port"])
    password = p["password"].encode('utf-8')
    conn = Client(address, authkey=password)

    if mode == "direct":
        conn.send("restart")
        status = conn.recv()
        if status == True: print("Successfully restarted.")
        else: print("Failed restarting.")
    elif mode == "fully":
        conn.send("close")
        print("Sent close.")
        print(start(path))

else:
    from multiprocessing.connection import Client
    p = c.getconfig("ci")
    address = ('localhost', p["port"])
    password = p["password"].encode('utf-8')
    try:
        conn = Client(address, authkey=password)
        conn.send(argument)
        if argument == "status":
            print(conn.recv())

        elif argument == "refresh_ndb":
            status = conn.recv()
            if status == True: print("Successfully refreshed NameDB.")
            else: print("Failed refreshing NameDB.")

        else:
            print("Sent " + argument + ".")

    except:
        print("Ground-Assistant is not running.")

sys.exit()
