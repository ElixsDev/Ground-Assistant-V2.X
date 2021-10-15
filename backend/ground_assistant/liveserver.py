class Server():
    def __init__(self, path):
        from ground_assistant.load import ReadConfig
        self.configs = ReadConfig(path)

        self.active = {}
        self.categorys = {"starting": [], "landing": [], "nearby": [], "faraway": []}

        from datetime import datetime
        self.dt = datetime

        from threading import Thread, Event
        self.cleanthread = Thread(target=self.cleaner, name="cleaner")
        self.cleanthread.start()
        self.stopevent = Event()

    def update(self, beacon):
        if "address" in self.active:
            self.active[beacon["address"]] = beacon
        else:
            self.active[beacon["address"]] = beacon

        from sys import stderr
        stderr.write(str(self.active))
        stderr.flush()
        return True

    def cleaner(self):
        from time import sleep
        from sys import stderr
        sleep(1)
        i = 0
        while not self.stopevent.is_set():
            stderr.write(str(i) + "\n")
            i += 1
            sleep(5)
            if i == 12:
                stderr.write("Hiooooo\n")
                self.clean(4)   #Executed every 12 loops = every 60s, flag reaction time is 5s
                i = 0

        return True

    def clean(self, age = 5):
        from sys import stderr
        for key in self.active:
            stamp = self.active[key]["timestamp"]
            delta = (self.dt.utcnow() - stamp).seconds
            stderr.write(str(delta) + "\n")
            if delta > int(age) * 60:
                stderr.write("remove " + str(active["key"]) + " because " + str(delta-5*60) + "\n")
                del active["key"]
        return True

    def close(self):
        self.stopevent.set()
        self.configs.close()
        from sys import stderr
        stderr.write("Closed\n")
        return True
