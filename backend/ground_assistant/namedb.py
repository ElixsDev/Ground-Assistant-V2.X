class NameDB:
    def __init__(self, path):
        import requests
        from multiprocessing import Process
        from ground_assistant.common.load import ReadConfig, mySQL
        config = ReadConfig(path)
        self.sql = mySQL(config)
        self.requests = requests
        self.prc = Process
        self.called = False
        self.sql_used = False
        self.refresh()

    def refresher(self):
        #Completely reset table
        self.sql.sendquery("DROP TABLE IF EXISTS ogn_name_db;")
        self.sql.sendquery("CREATE TABLE ogn_name_db " \
                           "(device_type VARCHAR(255), " \
                           "device_id VARCHAR(255), " \
                           "aircraft_model VARCHAR(255), " \
                           "registration VARCHAR(255), " \
                           "cn VARCHAR(255), " \
                           "tracked BOOL, " \
                           "identified BOOL);")
        self.sql.commit()

        for device in self.data: self.sql.sendquery('INSERT INTO ogn_name_db VALUES ' \
                                              f'("{device["device_type"]}",' \
                                              f'"{device["device_id"]}",' \
                                              f'"{device["aircraft_model"]}",' \
                                              f'"{device["registration"]}",' \
                                              f'"{device["cn"]}",' \
                                              f'{1 if device["tracked"] == "Y" else 0},' \
                                              f'{1 if device["identified"] == "Y" else 0});')
        self.sql.commit()
        self.sql.close() #connection is broken now anyways
        return


    def refresh_ndb(self, wait = False):
        if self.sql_used: return "still refreshing" if self.refreshprc.is_alive() else "already refreshed ndb"
        self.refresh()
        self.refreshprc = self.prc(target=self.refresher)
        self.refreshprc.start()
        self.sql_used = True
        if wait:
            from time import sleep
            while self.refreshprc.is_alive(): sleep(1)
            return "refreshed ndb"
        else: return "started refresher"

    def refresh(self):
        response = self.requests.get("http://ddb.glidernet.org/download/?j=1")
        if response.status_code != 200: return f'connection failed with code {response.status_code}'
        self.data = response.json()["devices"]
        return "refreshed ndb"

    def getname(self, device_id):
        empty = {"device_type": None, "device_id": device_id,
                 "aircraft_model": None, "registration": None,
                 "cn": None, "tracked": 0, "identified": 0}
        return next((sub for sub in self.data if sub["device_id"] == device_id), empty)

    def close(self):
        try:
            if self.refreshprc.is_alive():
                if not self.called: self.called = True; return "refresher is still running, call close again."
                else: self.refreshprc.kill()
            self.refreshprc.close()
        except AttributeError or ValueError: pass
        return "closed ndb"

def version():
    return "namedb.py: 2.0"
