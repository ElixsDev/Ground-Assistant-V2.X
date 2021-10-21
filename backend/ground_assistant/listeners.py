from ground_assistant.errorhandlers import *

class Listeners:
    def __init__(self):
        pass

    def forktolive(pipe):
        from setproctitle import setproctitle
        setproctitle("ga_forktolive")

        from ground_assistant.load import ReadConfig, mySQL
        from ground_assistant.logger import Logger  #Currently the config object is needed
        from ground_assistant.planelib import Library
        from multiprocessing.connection import Listener
        #from multithreading import Thread

        from sys import stderr
        stderr.write("1: Running...\n\n")

        kill = False
        wait = False
        init = False

        while kill == False:
            beacon = pipe.recv()

            if str(type(beacon)) == "<class 'str'>" and beacon[0:4] == "PATH" and init == False:
                path = beacon[4:]
                configs = ReadConfig(path)
                mysql = mySQL()
                logging = Logger(config_obj = configs, path = path, name = "forktolive.log")

                lib = Library(configs.getconfig("coordinates"), mysql)

                li = configs.getconfig("li")
                listener = Listener(('localhost', li["port"]), authkey=li["password"].encode('utf-8'))

                init = True
                logging.append("Started.")
                stderr.write("started.\n")
                continue

            elif beacon == "KILL":
                kill = True
                break
            elif beacon == "STOP":
                wait = True
                continue
            elif beacon == "CONTINUE":
                wait = False
                continue
            elif beacon == "SHOW":
                pr = []
                output = lib.output()
                for item in output:
                    pr.append(item[1][3])

                from sys import stderr
                stderr.write(str(pr) + "\n")
                continue

            if init == False:
                continue
            else:
                lib.add(beacon)

        if init == True:
            configs.close()
            mysql.close()
            listener.close()
            lib.close()
            logging.append("Closed.")
            logging.close()

        stderr.write("1: Ended\n\n")
        return

    def forktodb(pipe):
        from setproctitle import setproctitle
        setproctitle("ga_forktodb")

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
                #from sys import stderr
                #show = 5
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
