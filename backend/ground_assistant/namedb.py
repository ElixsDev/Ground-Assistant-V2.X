from ground_assistant.errorhandlers import *

class NameDB:
    def __init__(self,**kwargs):
        from multiprocessing import Process
        self.process = Process

        self.logging = kwargs["logging"]

        self.sql_raw = kwargs["sql"]
        self.sql_ready = self.sql_raw()

        self.logging.append("NameDB: ready")
        return

    def refresh_insertdb(self, json, sql_raw, logging):
        import time
        logging.append("NameDB: Refreshing...")

        sql = sql_raw()
        data = json["devices"]
        for devices in data:
            if devices["tracked"] == "Y":
                tracked = "1"
            else:
                tracked = "0"

            if devices["identified"] == "Y":
                identified = "1"
            else:
                identified = "0"

            command = {"INSERT INTO ogn_name_db VALUES (" +
                       "\"" + devices["device_type"] + "\"," +
                       "\"" + devices["device_id"] + "\"," +
                       "\"" + devices["aircraft_model"] + "\"," +
                       "\"" + devices["registration"] + "\"," +
                       "\"" + devices["cn"] + "\"," +
                       tracked + "," +
                       identified + ");"}
            command = ''.join(list(command))
            #logging.append(command)
            sql.sendquery(command)

        sql.commit()
        sql.close()
        return

    def refresh(self, retries = 3):
        import requests

        sql = self.sql_ready
        sql.sendquery("DROP TABLE IF EXISTS ogn_name_db;")
        command = {"CREATE TABLE IF NOT EXISTS ogn_name_db (" +
                   " device_type VARCHAR(255)," +
                   " device_id VARCHAR(255)," +
                   " aircraft_model VARCHAR(255)," +
                   " registration VARCHAR(255)," +
                   " cn VARCHAR(255)," +
                   " tracked BOOL," +
                   " identified BOOL);"}
        sql.sendquery(''.join(list(command)))
        sql.commit()

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

        inserting_process = self.process(target=self.refresh_insertdb, args=(response.json(), self.sql_raw, self.logging))
        inserting_process.start()
        return inserting_process

    def close(self):
        self.sql_ready.commit()
        self.sql_ready.close()
        return
