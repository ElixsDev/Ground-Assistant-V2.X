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
        #from ground_assistant.planeserver import server
        from multiprocessing.connection import Listener
        from threading import Thread
        from sys import stderr

        def server():
            while kill == False:
                with listener.accept() as connection:
                    request = connection.recv()
                    if request == "Stop Key: ljadljcg":
                        return

                    try:
                        response = lib.output(request)
                    except PlaneLibArgumentError:
                        response = "Invalid Argument(s): " + str(request)

                    connection.send(response)
            return

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
                serverthread = Thread(target=server)
                serverthread.start()

                init = True
                logging.append("Started.")
                #stderr.write("started.\n")
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

            if init == False:
                continue
            else:
                lib.add(beacon)

        if init == True:
            configs.close()
            mysql.close()

            from multiprocessing.connection import Client
            client = Client(('localhost', li["port"]), authkey=li["password"].encode('utf-8'))
            client.send("Stop Key: ljadljcg")
            client.close()
            serverthread.join()

            listener.close()
            lib.close()
            logging.append("Closed.")
            logging.close()

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
