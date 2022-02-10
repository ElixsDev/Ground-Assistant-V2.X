from ground_assistant.common.errorhandlers import *

class ReadConfig:
    def __init__(self, configpath, file = "ga.conf"):
        from os import path
        self.configpath = f'{configpath}/{file}'
        self.config = []

        if path.exists(self.configpath):
            configfile = open(self.configpath, "r")
            for line in configfile:
                x = line.strip()
                if x[:1] != "#": self.config.append(x)
            configfile.close()
        else: raise LoadError(f'Config file not found at {self.configpath}')

    def getconfig(self, type = None):
        if type == "all": return self.config

        elif type == "coordinates":
            return {"north": [float(self.config[1]), float(self.config[2])],
                    "east": [float(self.config[3]), float(self.config[4])],
                    "airport": self.config[5],
                    "altitude": int(self.config[6])}

        elif type == "runmode": return self.config[7]

        elif type == "mySQL":
            return {"username": self.config[8],
                    "password": self.config[9]}

        elif type == "ci": #Controll Interface
            return {"port": int(self.config[10]),
                    "password": self.config[11]}

        elif type == "li": #Live Interface
            return {"port": int(self.config[12]),
                    "password": self.config[13]}

        else: raise LoadError(f'Unknown argument "{str(type)}" for function getconfig()')

class mySQL:
    def __init__(self, configs):
        self.init(configs)

    def init(self, configs):
         import mysql.connector as sql
         self.InterfaceError = sql.errors.InterfaceError
         self.OperationalError = sql.errors.OperationalError

         credentials = configs.getconfig("mySQL")

         try: self.connection = sql.connect(host="localhost",
                                            user=credentials["username"],
                                            passwd=credentials["password"])
         except Exception as er: raise mySQLError(er) from None

         self.cursor = self.connection.cursor()
         self.cursor.execute("SHOW DATABASES;")
         res = self.cursor.fetchall()
         res = [x for sublist in res for x in sublist]
         if not "ogn" in res: self.cursor.execute("CREATE DATABASE ogn;")
         self.cursor.execute("use ogn;")
         return

    def sendquery(self, query):
        try:
            self.cursor.execute(query)
        except self.OperationalError:
            try:
                self.close()
                self.init()
                self.cursor.execute(query)
            except self.OperationalError as er:
                self.crashreport = er
                res = False

        try:
            res = self.cursor.fetchall()
            self.multiline = res
            res = [x for sublist in res for x in sublist]
        except self.InterfaceError as er:
            self.crashreport = er
            self.multiline = None
            res = False

        return res

    def commit(self):
        self.connection.commit()

    def close(self):
        self.connection.commit()
        self.cursor.close()
        self.connection.close()

def version():
    return "load.py: 4.0"
