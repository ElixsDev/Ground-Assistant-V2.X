from ground_assistant.errorhandlers import *

class Listeners:
    def __init__(self):
        pass

    def forktolive(pipe):
        from sys import stderr
        stderr.write("1: Running...\n\n")

        kill = False
        wait = False

        while kill == False:
            beacon = pipe.recv()
            if beacon == "KILL":
                kill = True
                break

            elif beacon == "STOP":
                wait = True
                continue
            elif beacon == "CONTINUE":
                wait = False
                continue

            stderr.write("1: " + str(beacon) + "\n\n")
        stderr.write("1: Ended\n\n")
        return

    def forktodb(pipe):
        from sys import stderr
        stderr.write("2: Running...\n\n")

        from datetime import datetime as dt
        from ground_assistant.dict import makedict as convert
        from ground_assistant.forktodb import MySQLLogger

        kill = False
        wait = False
        init = False

        while kill == False:
            beacon = pipe.recv()

            if beacon[0:4] == "PATH" and init == False:
                path = beacon[4:]
                logger = MySQLLogger(path)
                init = True
                continue

            if beacon == "KILL":
                kill = True
                break

            elif beacon == "STOP":
                wait = True
                continue
            elif beacon == "CONTINUE":
                wait = False
                continue

            if init == False:
                continue
            else:
                truebeacon = convert(dt, beacon)
                stderr.write(str(truebeacon))
                logger.write(truebeacon)
                stderr.write("2: Noted\n\n")

        if init == True: logger.close()
        stderr.write("2: Ended\n\n")
        return
