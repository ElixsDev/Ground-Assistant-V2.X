class NewPlane:
    def __init__(self, beacon, coordinates):
        self.parameters = coordinates
        self.cat_alt = {"tolerance": 5,
                        "landing": 150,
                        "nearby": 350}

        x = self.variables(beacon)
        if not x: raise KeyError
        self.categorize()

    def variables(self, beacon):
        try:
            self.raw_message = beacon["raw_message"]

            self.aprs_info = {"aprs_type": beacon["aprs_type"],
                              "beacon_type": beacon["beacon_type"],
                              "address_type": beacon["address_type"],
                              "receiver:name": beacon["receiver_name"],
                              "relay": beacon["relay"],
                              "dstcall": beacon["dstcall"]}

            self.identity = {"address": beacon["address"],
                             "aircraft_type": beacon["aircraft_type"],
                              "name": beacon["name"]}

            self.position = {"latitude": beacon["latitude"],
                             "longitude": beacon["longitude"]}

            self.vectors = {"altitude": beacon["altitude"],
                            "ground_speed": beacon["ground_speed"],
                            "turn_rate": beacon["turn_rate"],
                            "climb_rate": beacon["climb_rate"]}

            self.timestamps = {"timestamp": beacon["timestamp"],
                               "reference_timestamp": beacon["reference_timestamp"]}

            self.permissions = {"stealth": beacon["stealth"],
                                "no_tracking": not beacon["no-tracking"]}

            self.signal = {"quality": beacon["signal_quality"],
                           "frequency_offset": beacon["frequency_offset"]}
                           #"gps_quality": beacon["gps_quality"]}

            self.others = {"symboltable": beacon["symboltable"],
                           "symbolcode": beacon["symbolcode"],
                           "comment": beacon["comment"],
                           "track": beacon["track"]}

        except KeyError:
            return False

        #self.error_count = beacon["error_count"]
        return True

    def categorize(self):
        if self.vectors["altitude"] <= self.parameters["altitude"] + self.cat_alt["tolerance"]:
            alt = "grounded"
        elif self.vectors["altitude"] <= self.parameters["altitude"] + self.cat_alt["landing"] + self.cat_alt["tolerance"]:
            alt = "landing"
        elif self.vectors["altitude"] <= self.parameters["altitude"] + self.cat_alt["nearby"] + self.cat_alt["tolerance"]:
            alt = "nearby"
        else:
            alt = "away"

        geo = "unknown"
        if self.position["latitude"] <= self.parameters["north"][0]:
            if self.position["latitude"] >= self.parameters["north"][1]:
                if self.position["longitude"] <= self.parameters["east"][0]:
                    if self.position["longitude"] >= self.parameters["east"][1]:
                        geo = self.parameters["airport"]

        self.categorys = {"alt": alt,
                          "geo": geo}

    def update(self, beacon):
        x = self.variables(beacon)
        if not x: raise KeyError
        self.categorize()
        return True

    def is_not_expired(self, age = 5):
        from datetime import datetime
        if (datetime.utcnow() - self.timestamps["timestamp"]).seconds > age * 60: return False
        else: return True

    def close(self):
        return True
