class NewPlane:
    def __init__(self, beacon, airports, ndb):
        self.airports = airports
        self.ndb = ndb
        self.types = ["?", "(Moto-) Glider", "Tow Plane", "Helicopter", "Parachute", "Drop Plane", "Hang-Glider",
                      "Para-Glider", "Powered Aircraft", "Jet Aircraft", {"A": "UFO", "B": "Balloon",
                      "C": "Airship", "D": "UAV", "E": "Ground-Support", "F": "Static Object"}]
        self.categorys = {"geo": None}
        self.update(beacon)

    def update(self, beacon):
        #Write data into variables
        self.raw_message = beacon["raw_message"]

        self.aprs_info = {"aprs_type": beacon["aprs_type"] if "aprs_type" in beacon.keys() else None,
                          "beacon_type": beacon["beacon_type"] if "beacon_type" in beacon.keys() else None,
                          "address_type": beacon["address_type"] if "address_type" in beacon.keys() else None,
                          "receiver_name": beacon["receiver_name"] if "receiver_name" in beacon.keys() else None,
                          "relay": beacon["relay"] if "relay" in beacon.keys() else None,
                          "dstcall": beacon["dstcall"] if "dstcall" in beacon.keys() else None}

        self.position = {"latitude": beacon["latitude"] if "latitude" in beacon.keys() else None,
                         "longitude": beacon["longitude"] if "longitude" in beacon.keys() else None}

        self.vectors = {"altitude": beacon["altitude"] if "altitude" in beacon.keys() else None,
                        "ground_speed": beacon["ground_speed"] if "ground_speed" in beacon.keys() else None,
                        "turn_rate": beacon["turn_rate"] if "turn_rate" in beacon.keys() else None,
                        "climb_rate": beacon["climb_rate"] if "climb_rate" in beacon.keys() else None}

        self.timestamps = {"timestamp": beacon["timestamp"] if "timestamp" in beacon.keys() else None,
                           "reference_timestamp": beacon["reference_timestamp"] if "reference_timestamp" in beacon.keys() else None}

        self.permissions = {"stealth": beacon["stealth"] if "stealth" in beacon.keys() else None,
                            "no_tracking": not beacon["no-tracking"] if "no-tracking" in beacon.keys() else None}

        self.signal = {"signal_quality": beacon["signal_quality"] if "signal_quality" in beacon.keys() else None,
                       "frequency_offset": beacon["frequency_offset"] if "frequenzy_offset" in beacon.keys() else None,
                       "gps_quality": [beacon["gps_quality"]["vertical"],
                                       beacon["gps_quality"]["horizontal"]] if "gps_quality" in beacon.keys() else None}

        self.others = {"comment": beacon["comment"] if "comment" in beacon.keys() else None,
                       "track": beacon["track"] if "track" in beacon.keys() else None}

        self.error_count = beacon["error_count"] if "error_count" in beacon.keys() else None

        self.identity = {"address": beacon["address"] if "address" in beacon.keys() else None,
                         "aircraft_type": beacon["aircraft_type"] if "aircraft_type" in beacon.keys() else None,
                         "name": beacon["name"] if "name" in beacon.keys() else None}

        device_id = beacon["address"]
        planedata = self.ndb(device_id)
        self.identity = {"device_id": device_id}

        type = beacon["aircraft_type"]
        self.identity["aircraft_type"] = self.types[type] if isinstance(type, int) else self.types[10][type]
        self.identity["aircraft_model"] = planedata["aircraft_model"]
        self.identity["registration"] = planedata["registration"]
        self.identity["cn"] = planedata["cn"]
        self.identity["identified"] = True if planedata["identified"] == "Y" else False

        #Categorize:
        airport = self.airports.find(self.position, self.categorys["geo"])
        if airport:
            altitude = self.vectors["altitude"] - airport[1]["altitude"] - airport[1]["cat_alt"][0]
            self.categorys["geo"] = airport[0]

            if altitude <= 0: alt = "grounded"
            elif altitude <= airport[1]["cat_alt"][1]: alt = "landing"
            elif altitude <= airport[1]["cat_alt"][2]: alt = "nearby"
            elif altitude > airport[1]["cat_alt"][2]: alt = "away"
            self.categorys["alt"] = alt

        else: self.categorys = {"geo": None, "alt": "away"}

        self.relevant = {"receiver_name": self.aprs_info["receiver_name"],
                         "timestamp": str(self.timestamps["timestamp"])}

        self.relevant.update(self.identity)
        self.relevant.update(self.position)
        self.relevant.update(self.vectors)
        self.relevant.update(self.signal)
        return

    def is_expired(self, age = 5):
        from datetime import datetime
        if (datetime.utcnow() - self.timestamps["timestamp"]).seconds > age * 60: return True
        else: return False
