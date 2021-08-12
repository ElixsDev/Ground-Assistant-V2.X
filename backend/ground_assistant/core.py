from ground_assistant.errorhandlers import *

class Core:
    def __init__(self,**kwargs):
        from ground_assistant.load import ReadConfig, mySQL
        from ground_assistant.log  import Logger

        from os.path import abspath
        path = abspath(".")

        configs = ReadConfig("/home/elias/dev/ground-assistant/daemon")                                             #Change to path var when finished
        self.configs = configs

        logging = Logger(config_obj = configs, path = "/home/elias/dev/ground-assistant/backend/ground_assistant")  #Change to path var when finished
        self.logging = logging

        logging.append("Starting...")

        sql = mySQL()
        self.sql = sql
        sql.sendquery("SHOW TABLES;")

    def refresh_namedb(self, retries = 3):
        import requests

        self.sql.sendquery("DROP TABLE IF EXISTS ogn_name_db;")

        command = {"CREATE TABLE IF NOT EXISTS ogn_name_db (" +
                   " device_type VARCHAR(255)," +
                   " device_id VARCHAR(255)," +
                   " aircraft_model VARCHAR(255)," +
                   " registration VARCHAR(255)," +
                   " cn VARCHAR(255)," +
                   " tracked BOOL," +
                   " identified BOOL);"}

        self.sql.sendquery(''.join(list(command)))

        while retries > 0:
            retries -= 1
            try:
                response = requests.get("http://ddb.glidernet.org/download/?j=1")
                if str(response) != "<Response [200]>": raise httpError("Unable to get json file from ddb.glidernet.org: " + str(response))
                break

            except httpError:
                pass
        else:
            raise httpError("Unable to connect to ddb.glidernet.org")

        json = response.json()
        return json


    def nsprocess():
        pass

    def close(self):
        self.sql.commit()
        self.sql.close()
        self.logging.append("Daemon stopped.")
        self.logging.close()

def version():
    return "core.py: 1.0"

c = Core()
c.refresh_namedb()
c.close()
