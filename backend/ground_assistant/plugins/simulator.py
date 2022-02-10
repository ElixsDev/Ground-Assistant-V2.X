#Simulates data from ogn network

mark = "" #Prevents from beeing registered as normal plugin

port = 5009
word = "fakeyou"

class Receiver:
    def __init__(self, pipe, path):
        self.path = path
        self.p_send = pipe #Pipe to the distr center

    def init(self):
        from threading import Thread
        from multiprocessing.connection import Listener
        address = ("localhost", port)     # family is deduced to be 'AF_INET'
        password = word.encode("utf-8")
        self.listener = Listener(address, authkey=password)

        self.emitterthread = Thread(target = self.emitter, name = "FakeEmitter")
        return True

    def emitter(self):
        from time import sleep
        keepalive = True

        while keepalive:
            connection = self.listener.accept()
            connected = True
            while connected:
                try: config = connection.recv()
                except EOFError: connected = False; continue
                if config == "exit": keepalive = False; break
                beacon = config[0]
                self.p_send.send(beacon)
                connection.send("Started...")
                for item in config[1]:
                    beacon = item[0]
                    self.p_send.send(beacon)
                    sleep(item[1])
                connection.send("Done")
        return

    def run(self):
        self.emitterthread.start()
        return

    def close(self):
        try: self.listener.close()
        except AttributeError: pass

        try:
            self.emitterthread.join(1)
            if self.emitterthread.is_alive():
                from multiprocessing.connection import Client
                con = Client(('localhost', port), authkey=word.encode('utf-8'))
                con.send("exit")
                con.close()
                self.emitterthread.join(5)
        except AttributeError: pass
        return

class BeaconConfig:
    def __init__(self, address = "DDD222", north = 49.5, east = 8.5):
        from datetime import datetime
        self.dt = datetime
        self.movement = []
        self.beacon = {"raw_message": "This is a test beacon. It doesn't contain real data.",
                       "reference_timestamp": datetime.utcnow(),
                       "aprs_type": "position",
                       "dstcall": "APRS",
                       "relay": None,
                       "receiver_name": "EGHL",
                       "timestamp": datetime.utcnow(),
                       "track": 86,
                       "ground_speed": 100,
                       "altitude": 95,
                       "address_type": 2,
                       "aircraft_type": 1,
                       "no-tracking": False,
                       "stealth": False,
                       "climb_rate": 0.0,
                       "turn_rate": 0.0,
                       "signal_quality": 5.5,
                       "error_count": 3,
                       "frequency_offset": -4.3,
                       "beacon_type": "flarm"}
        self.setname(name)
        self.setposition(north, east)
        self.setmovement()

    def setname(self, name):
        self.beacon["address"] = name.upper()
        self.beacon["name"] = f'FLR{name.upper()}'
        return

    def setposition(self, north, east):
        self.beacon["latitude"] = north
        self.beacon["longitude"] = east
        return

    def resettime(self):
        self.beacon["timestamp"] = self.dt.utcnow()
        self.beacon["reference_timestamp"] = self.dt.utcnow()
        return

    def setexpired(self):
        yesterday = self.dt.utcnow().date() - self.dt.timedelta(days=1)
        self.beacon["timestamp"] = yesterday
        self.beacon["reference_timestamp"] = yesterday
        return

    def setmovement(self, step = 0.0001, intervall = 1, moves = 500):
        from copy import deepcopy
        original = deepcopy(self.beacon)
        self.movement = []
        for i in range(1, moves):
            self.beacon["latitude"] = round(self.beacon["latitude"] + step, 4)
            self.beacon["longitude"] = round(self.beacon["longitude"] + step, 4)
            self.movement.append([deepcopy(self.beacon), intervall])
        self.beacon = original
        return

    def config(self):
        return [self.beacon, self.movement]

class TestHelper:
    def __init__(self):
        from multiprocessing.connection import Client
        self.bc = BeaconConfig()
        self.beacon = self.bc.config()
        self.con = Client(('localhost', port), authkey=word.encode('utf-8'))

    def send(self, beacon = None):
        if not beacon: beacon = self.beacon
        self.con.send(beacon)
        self.con.recv()
        self.con.recv()
        return
