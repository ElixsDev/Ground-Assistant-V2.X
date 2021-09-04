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

    def forktodb(pipe):
        from sys import stderr
        stderr.write("2: Running...\n\n")

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

            stderr.write("2: " + str(beacon) + "\n\n")
        stderr.write("2: Ended\n\n")
