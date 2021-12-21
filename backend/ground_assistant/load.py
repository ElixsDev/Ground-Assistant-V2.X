from ground_assistant.errorhandlers import *

class ReadConfig:
    def __init__(self, configpath):
        import os
        configpath = configpath + "/ga.conf"
        self.configpath = configpath

        global config
        config = []

        if os.path.exists(configpath):
            configfile = open(configpath, "r")
            for zeile in configfile:
                x = zeile.strip()
                if x[:1] != "#":
                    config.append(x)
            configfile.close()
        else:
            raise LoadError("Config file not found at " + configpath)

        if len(config) != 14: raise LoadError("Config file is corrupted (" + len(config) + " lines)")
        self.config = config

    def getconfig(self, type = None):
        if isinstance(self, str) and type == None:         #Error bypass: bypasses error when mySQL class calls ReadConfig.getconfig(type)
            type = self

        if type == "coordinates":
            return {"north": [float(config[1]), float(config[2])], "east": [float(config[3]), float(config[4])], "airport": config[5], "altitude": int(config[6])}
        elif type == "runmode":
            return config[7]
        elif type == "mySQL":
            return {"username": config[8], "password": config[9]}
        elif type == "ci": #Controll Interface
            return {"port": int(config[10]), "password": config[11]}
        elif type == "li": #Live Interface
            return {"port": int(config[12]), "password": config[13]}
        else:
            raise LoadError("Unknown argument \"" + str(type) + "\" for function getconfig()")

    def close(self):
        return True

class mySQL:
    def __init__(self):
         import mysql.connector as sql
         global sql

         try:
             credentials = ReadConfig.getconfig("mySQL")
         except NameError:
             raise LoadError("Called mySQL class before calling ReadConfig class")

         try:
             connection = sql.connect(host="localhost", user=credentials["username"], passwd=credentials["password"])
             self.connection = connection
         except Exception as error:
             raise mySQLError(error) from None

         cursor = connection.cursor()
         self.cursor = cursor
         cursor.execute("SHOW DATABASES;")
         res = cursor.fetchall()
         res = [x for sublist in res for x in sublist]

         try:
             res.index("ogn")
         except:
             cursor.execute("CREATE DATABASE ogn;")

         cursor.execute("use ogn;")

    def sendquery(self, query):
        self.cursor.execute(query)
        try:
            res = self.cursor.fetchall()
            self.multiline = res
            res = [x for sublist in res for x in sublist]
        except sql.errors.InterfaceError:
            self.multiline = None
            res = None

        return res

    def commit(self):
        self.connection.commit()

    def close(self):
        self.connection.commit()
        self.cursor.close()
        self.connection.close()

def version():
    return "load.py: 3.0"
