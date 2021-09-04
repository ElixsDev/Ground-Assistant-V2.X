class Daemon:
    def __init__(self):
        from ground_assistant import Core
        from os.path import abspath
        self.c = Core(path=abspath("."))

    def prepare(self):
        from multiprocessing import Process
        self.listeners = self.c.open_mouth()
        self.screamer = self.c.aprs()
        self.screamer_process = Process(target=self.screamer.run, kwargs={"callback": self.c.scream, "autoreconnect": True,})
        self.refreshed = False #Variable isnt set in init to cause refresh_ndb() to crash if it is executed before prepare()
        return True

    def run(self):
        self.screamer_process.start()
        return True

    def refresh_ndb(self, ifnotdoneyet = False):
        if ifnotdoneyet == True and self.refreshed == True:
            return False

        self.c.pipes["live"].send("STOP")
        self.c.pipes["db"].send("STOP")
        refreshing = self.c.ndb.refresh()
        refreshing.join()
        self.c.pipes["live"].send("CONTINUE")
        self.c.pipes["db"].send("CONTINUE")
        self.refreshed = True
        return True

    def close(self):
        self.c.close()
        self.screamer_process.kill()
        self.screamer_process.close()
        return True
