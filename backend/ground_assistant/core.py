from ground_assistant.errorhandlers import *

class Core:
    def __init__(self, **kwargs):
        from ground_assistant.load import ReadConfig, mySQL
        from ground_assistant.logger  import Logger
        from ground_assistant.namedb import NameDB

        configs = ReadConfig(kwargs["path"])
        self.configs = configs
        self.coordinates = configs.getconfig("coordinates")

        self.logging = Logger(config_obj = configs, path = kwargs["path"], name = "ga.conf")
        self.aprs_logging = Logger(config_obj = configs, path = kwargs["path"], name = "aprs_error.log")

        self.logging.append("Starting...")

        sql = mySQL()
        self.sql = sql
        sql.sendquery("SHOW TABLES;")
        self.logging.append("Core MySQL: ready")

        self.ndb = NameDB(sql = mySQL, logging = self.logging)                                                           #The ndb object has its own mySQL connection

    def aprs(self):
        try:
            from ogn.client import AprsClient
            from ogn.parser import parse, ParseError

        except ImportError:
            self.success = False
            self.logging.append("Python package \"ogn-client\" missing")
            return

        self.aprs_parse = parse
        self.aprs_error = ParseError
        self.client = AprsClient(aprs_user='N0CALL')
        self.client.connect()

        self.success = True
        self.logging.append("Core APRS: ready")

        return self.client

    def open_mouth(self):
        from ground_assistant.listeners import Listeners
        from multiprocessing import Process, Pipe
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
        self.logging.append("Forking Processes: running")

        return self.processes

    def scream(self, raw_message):
        try:
            beacon = self.aprs_parse(raw_message)
        except self.aprs_error as message:
            self.aprs_logging.append(str(message))
            return

        if beacon["aprs_type"] == "position" and beacon["beacon_type"] == "flarm":
            if float(beacon["latitude"]) <= float(self.coordinates["north"][0]) and float(beacon["latitude"]) >= float(self.coordinates["north"][1]):
                if float(beacon["longitude"]) <= float(self.coordinates["east"][0]) and float(beacon["longitude"]) >= float(self.coordinates["east"][1]):
                    self.pipes["live"].send(beacon)
                    self.pipes["db"].send(beacon)
        return

    def close(self):
        self.logging.append("Stopping...")


        self.pipes["live"].send("KILL")
        self.pipes["db"].send("KILL")

        self.processes["live"].join()
        self.processes["db"].join()

        self.processes["live"].close()
        self.processes["db"].close()
        self.logging.append("Forking Processes: stopped")


        self.client.disconnect()
        self.logging.append("Core APRS: disconnected")

        self.ndb.close()
        self.logging.append("Core NameDB: closed")

        self.sql.commit()
        self.sql.close()
        self.logging.append("Core MySQL: closed")
        self.logging.append("Daemon stopped.")
        self.logging.close()

def version():
    return "core.py: 1.0"
