mark = "plugin_db"

def main(pipe, path, ndb):
    from setproctitle import setproctitle
    setproctitle(mark)

    from datetime import datetime as dt
    from ground_assistant.plugins.sqllogger import MySQLLogger

    keepalive = True
    wait = False
    init = True
    show = 0

    logger = MySQLLogger(path)

    while keepalive:
        beacon = pipe.recv()
        if isinstance(beacon, str):
            if beacon[:4] == "KILL":
                if beacon[4:] == mark:
                    kill = True
                    break
                else:
                    continue

            elif beacon == "STOP":
                wait = True
                continue
            elif beacon == "CONTINUE":
                wait = False
                continue
            elif beacon == "SHOW":
                from sys import stderr
                show = 5
                continue

        if init == False: continue
        if show > 0:
            stderr.write("1: " + str(beacon) + "\n")
            show -= 1
        logger.write(beacon)

    if init == True: logger.close()
    return
