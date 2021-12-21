from ground_assistant.errorhandlers import *

class Library:
    def __init__(self, coordinates, mysql):
        from datetime import datetime
        from ground_assistant.plane import NewPlane
        self.datetime = datetime
        self.newplane = NewPlane
        self.mysql = mysql
        self.coordinates = coordinates
        self.index = {}

    def add(self, beacon):
        try:
            if not beacon["address"] in self.index.keys():
                self.index[beacon["address"]] = self.newplane(beacon, self.coordinates)
            else:
                self.index[beacon["address"]].update(beacon)
        except KeyError:
            return False
        return True

    def clean(self, age = 5):
        rem = []
        for key in self.index:
            if not self.index[key].is_not_expired(age = age):
                rem.append(key)

        for key in rem:
            self.index[key].close()
            del self.index[key]

        return True

    def output(self, request = {"geocat": "EDFM", "altcat": "grounded"}):
        ret = {}
        rem = []

        if type(request) is not dict: raise PlaneLibArgumentError("Request should be a dictionary")

        for key in self.index:
            if self.index[key].categorys["geo"] == request["geocat"] and self.index[key].is_not_expired():
                if self.index[key].categorys["alt"] == request["altcat"]:
                    ret[key] = [None, self.index[key]]

            elif not self.index[key].is_not_expired():
                rem.append(key)

        for key in ret:
            device_id = key
            query = "SELECT * FROM ogn_name_db WHERE device_id = \"" + device_id + "\";"
            result = self.mysql.sendquery(query)
            ret[key][0] = result

        for key in rem:
            self.index[key].close()
            del self.index[key]

        return ret

    def debug(self):
        return self.index

    def close(self):
        for key in self.index:
            self.index[key].close()
        return True
