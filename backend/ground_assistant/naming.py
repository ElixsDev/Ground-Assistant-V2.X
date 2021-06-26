#Version: 1.0, Copyright: EliServices

class NameDB:
    def __init__(self):
        global os, sys, ctime, log, config, db, dbc
        import os, sys
        from time import ctime
        from ground_assistant.load import load

        path = os.path.abspath(".")

        config = load(path)                                                #Settings are beeing loaded from configfile and MySQL is beeing prepared
        db = load.db                                                       #Transfer sql object
        dbc = db.cursor()

        if config[1] == "console":                                         #Redirect output to console
            log = sys.stderr
        elif config[1] == "logfile":                                       #Redirect output to logfile
            log = open(path + "/NameDB.log", "a")
        else:                                                              #No output, but still write method (makes it easier)
            log = open("/dev/null", "a")

        log.write(ctime().split()[3] + ": Started: Success.\n")
        log.flush()

    def refresh(self,retries=2):
        log.write(ctime().split()[3] + ": Refreshing...\n")
        log.flush()
        import requests

        command = {"CREATE TABLE IF NOT EXISTS ogn_name_db (" +
                   " device_type VARCHAR(255)," +
                   " device_id VARCHAR(255)," +
                   " aircraft_model VARCHAR(255)," +
                   " registration VARCHAR(255)," +
                   " cn VARCHAR(255)," +
                   " tracked BOOL," +
                   " identified BOOL);"}

        dbc.execute(''.join(list(command)))                                      #Execute the command
        dbc.execute("DELETE FROM ogn_name_db;")

        try:
            response = requests.get("http://ddb.glidernet.org/download/?j=1")
        except Exception as er:
            while er != None and retries > 0:
                er = None
                retries -= 1
                log.write(ctime().split()[3] + ": Refreshing: Failed to get file, trying again...\n")
                try:
                    response = requests.get("http://ddb.glidernet.org/download/?j=1")
                except:
                    er = "Not None"

            if er != None:
                log.write(ctime().split()[3] + ": Refreshing: Failed.\n")
                return False

        data = response.json()["devices"]
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

            dbc.execute(''.join(list(command)))                                      #Execute the command

        db.commit()
        log.write(ctime().split()[3] + ": Refreshing: Success.\n")
        log.flush()
        return

    def identify(self,flarm):
        dbc.execute("SELECT * FROM ogn_name_db WHERE device_id = \"" + flarm + "\";")
        row = list(dbc.fetchall())
        row = [x for sublist in row for x in sublist]
        return row

    def close(self):
        db.close()
        log.write(ctime().split()[3] + ": Exiting: Success.\n")
        log.flush()
        log.close()                                                                                   #Close logfile
        return
