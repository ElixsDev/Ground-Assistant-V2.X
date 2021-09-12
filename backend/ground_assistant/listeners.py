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

            #stderr.write("1: " + str(beacon) + "\n\n")
        stderr.write("1: Ended\n\n")
        return

    def forktodb(pipe):
        from datetime import datetime as dt
        from ground_assistant.forktodb import MySQLLogger

        kill = False
        wait = False
        init = False
        show = 0

        while kill == False:
            beacon = pipe.recv()

            if str(type(beacon)) == "<class 'str'>" and beacon[0:4] == "PATH" and init == False:
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
            elif beacon == "SHOW":
                from sys import stderr
                show = 10
                continue

            if init == False:
                continue
            else:
                if show > 0:
                    stderr.write("1: " + str(beacon) + "\n")
                    show -= 1
                logger.write(beacon)

        if init == True: logger.close()
        return
