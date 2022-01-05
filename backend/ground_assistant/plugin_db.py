mark = "plugin_db"

def main(pipe, path):
    from setproctitle import setproctitle
    setproctitle("plugin_db")

    from datetime import datetime as dt
    from ground_assistant.forktodb import MySQLLogger

    keepalive = True
    wait = False
    init = True
    show = 0

    logger = MySQLLogger(path)

    while keepalive:
        beacon = pipe.recv()

        #if str(type(beacon)) == "<class 'str'>" and beacon[0:4] == "PATH" and init == False:
        #    path = beacon[4:]
        #    logger = MySQLLogger(path)
        #    init = True
        #    continue

        if beacon[:4] == "KILL":
            if beacon[4:] == "plugin_db":
                kill = True
                break
            else:
                continue

        if beacon == "STOP":
            wait = True
            continue
        elif beacon == "CONTINUE":
            wait = False
            continue
        elif beacon == "SHOW":
            #from sys import stderr
            #show = 5
            continue

        if init == False:
            continue
        else:
            if show > 0:
                stderr.write("1: " + str(beacon) + "\n")
                show -= 1
            #logger.write(beacon)
            print("potential write")

    if init == True: logger.close()
    return
