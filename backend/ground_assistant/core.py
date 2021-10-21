from ground_assistant.errorhandlers import *

class Core:
    def __init__(self, path, mode = "startup"):
        global ReadConfig, mySQL, Logger, NameDB
        from ground_assistant.load import ReadConfig, mySQL
        from ground_assistant.logger  import Logger
        from ground_assistant.namedb import NameDB

        self.path = path
        configs = ReadConfig(path)
        self.configs = configs
        self.coordinates = configs.getconfig("coordinates")

        self.logging = Logger(config_obj = configs, path = path, name = "ga.log")
        self.aprs_logging = Logger(config_obj = configs, path = path, name = "aprs_error.log")

        if mode == "startup": self.logging.append("Starting...")
        if mode == "restart": self.logging.append("Daemon restarting...")

        sql = mySQL()
        self.sql = sql
        sql.sendquery("SHOW TABLES;")
        self.logging.append("Core MySQL: ready")

        self.ndb = NameDB(sql = mySQL, logging = self.logging)    #The ndb object has its own mySQL connection
        self.clientready = False
        self.pipesready = False
        return

    def aprs(self):
        try:
            from ogn.client import AprsClient
            from ogn.parser import parse, ParseError

        except ImportError:
            self.logging.append("Python package \"ogn-client\" missing")
            return

        self.aprs_parse = parse
        self.aprs_error = ParseError
        self.client = AprsClient(aprs_user='N0CALL')
        self.client.connect()
        self.logging.append("Core APRS: ready")

        self.clientready = True
        if self.pipesready == True: self.logging.append("Daemon ready to run.")
        return self.client

    def open_mouth(self):
        from ground_assistant.listeners import Listeners
        from multiprocessing import Process, Pipe
        from time import sleep

        live_receive, live_send = Pipe()
        db_receive, db_send = Pipe()
        self.pipes = {"live": live_send, "db": db_send}
        self.logging.append("Forking Pipes: ready")

        live_process = Process(target=Listeners.forktolive, args=(live_receive, ))
        db_process = Process(target=Listeners.forktodb, args=(db_receive, ))
        self.logging.append("Forking Processes: ready")

        live_process.start()
        db_process.start()
        self.processes = {"live": live_process, "db": db_process}

        sleep(2)
        Listeners = None   #Needed for restart (?)
        live_send.send("PATH" + self.path)
        db_send.send("PATH" + self.path)
        self.logging.append("Forking Processes: running")

        self.pipesready = True
        if self.clientready == True: self.logging.append("Daemon ready to run.")
        return self.processes

    def scream(self, raw_message):
        try:
            beacon = self.aprs_parse(raw_message)
        except Exception as message: #self.aprs_error as message:
            self.aprs_logging.append(str(message))
            return

        if beacon["aprs_type"] == "position" and beacon["beacon_type"] == "flarm" and beacon["aircraft_type"] == 1:
            self.pipes["live"].send(beacon)
            self.pipes["db"].send(beacon)
        return

    def close(self, mode = "close"):
        self.logging.append("Stopping...")

        if self.pipesready == True:
            if self.processes["db"].is_alive():
                self.pipes["db"].send("KILL")
                self.processes["db"].join()
            self.processes["db"].close()

            if self.processes["live"].is_alive():
                self.pipes["live"].send("KILL")
                self.processes["live"].join()
            self.processes["live"].close()

            self.logging.append("Forking Processes: stopped")
        else:
            self.logging.append("Forking Processes: never started")

        if self.clientready == True:
            self.client.disconnect()
            self.logging.append("Core APRS: disconnected")
        else:
            self.logging.append("Core APRS: never connected")

        self.ndb.close()
        self.logging.append("Core NameDB: closed")

        self.sql.commit()
        self.sql.close()
        self.logging.append("Core MySQL: closed")
        if mode == "close": self.logging.append("Daemon stopped.")
        if mode == "restart": self.logging.append("Daemon ready to restart.")
        self.logging.close()
        return

def version():
    return "core.py: 1.0"
