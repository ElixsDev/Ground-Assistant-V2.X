import sys

if len(sys.argv) > 2:
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

if argument == "help":
    print("""  usage: ground-assistant [-action]
  -------------------- actions ---------------------
  --start        start the daemon
  --stop         temporarily stops the data input
  --continue     continue data input after stop
  --close        stop ground-assistant daemon
  --restart      restart ground-assistant daemon
  --status       send status request
  --show         show 10 beacons from data input
  --refresh_ndb  refreshes NameDB
  --help         show this help""")

elif argument == "start":
    import os
    os.system("python " + os.path.abspath(".") + "/ground-assistant.py &")
    print("Started Ground-Assistant.")

else:
    from multiprocessing.connection import Client
    authkey = b'ground-assistant-ipc'
    address = ('localhost', 6000)
    try:
        conn = Client(address, authkey=authkey)
        conn.send(argument)
        if argument == "status":
            print(conn.recv())
        elif argument == "restart":
            status = conn.recv()
            if status == True: print("Successfully restarted.")
            else: print("Failed restarting.")
        elif argument == "refresh_ndb":
            status = conn.recv()
            if status == True: print("Successfully refreshed NameDB.")
            else: print("Failed refreshing NameDB.")
        else:
            print("Send " + argument)
    except:
        print("Ground-Assistant is not running.")

sys.exit()
