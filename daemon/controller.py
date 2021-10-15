class Controller:
    def __init__(self, path, mode = "quickstart"):
        from os import getpid
        self.path = path

        from ground_assistant import Core
        self.c = Core(self.path, mode = "startup")
        self.logging = self.c.logging
        self.ipc_activated = False
        self.closed = False
        self.prepared = False
        self.restarted = 0

        if mode == "quickstart":
            self.prepare()
            self.run()

    def prepare(self):
        if self.closed == True: return False
        global Process
        from multiprocessing import Process
        self.listeners = self.c.open_mouth()
        self.screamer = self.c.aprs()
        self.screamer_process = Process(target=self.screamer.run, kwargs={"callback": self.c.scream, "autoreconnect": True,})
        self.refreshed = False #Variable isnt set in init to cause refresh_ndb() to crash if it is executed before prepare()
        self.running = False
        self.prepared = True
        return True

    def ipc(self, port, password):
        if self.closed == True: return False
        if self.ipc_activated == True: return False

        from multiprocessing.connection import Listener
        address = ('localhost', port)     # family is deduced to be 'AF_INET'
        self.listener = Listener(address, authkey=password.encode('utf-8'))
        self.ipc_activated = True
        return self.listener

    def run(self):
        if self.closed == True: return False
        self.screamer_process.start()
        self.logging.append("Started screaming...")
        self.running = True
        return True

    def stop(self):
        if self.closed == True: return False
        self.screamer_process.kill()
        self.screamer_process.join()
        self.screamer_process.close()
        self.screamer_process = None
        self.screamer_process = Process(target=self.screamer.run, kwargs={"callback": self.c.scream, "autoreconnect": True,})
        self.logging.append("Stoped screaming.")
        self.running = False
        return True

    def restart(self):
        if self.closed == True: return False
        self.logging.append("Triggered Restart...")
        self.stop()
        self.prepared = False
        self.c.close(mode = "restart")

        del self.c
        from ground_assistant.core import Core

        self.c = Core(self.path, mode = "restart")
        self.logging = self.c.logging
        self.prepare()
        self.run()
        self.logging.append("Restart complete.")
        self.restarted += 1
        return True

    def close(self):
        if self.closed == True: return False
        if self.ipc_activated == True: self.listener.close()
        self.stop()
        self.c.close(mode = "close")
        self.closed = True
        return True

    def status(self, mode = "return"):
        if self.closed == True:
             return "Daemon was stopped."

        if self.prepared == False:
            status = "Daemon is ready to be prepared."
        else:
            if self.refreshed == False:
                refreshed = "NameDB was not refreshed yet."
            else:
                refreshed = "NameDB was last refreshed on " + self.refreshed

            if self.running == False:
                status = "Daemon is prepared and ready to run, "
            else:
                status = "Daemon is running, "

            status += refreshed + "\nWe had " + str(self.restarted) + " restarts."

            if self.listeners["live"].is_alive() == True:
                status += "\n Listener \"live\" is alive."
            else:
                status += "\n Listener \"live\" is dead."

            if self.listeners["db"].is_alive() == True:
                status += "\n Listener \"db\" is alive."
            else:
                status += "\n Listener \"db\" is dead."

            try:
                if self.screamer_process.is_alive() == True:
                    status += "\n Screamer is alive."
                else:
                    status += "\n Screamer is dead."
            except:
                status += "\n Screamer is dead."

        if mode == "dual":
            self.logging.append("Requested status:\n" + status + "\n")
            return status
        elif mode == "logfile":
            self.logging.append("Requested status:\n" + status + "\n")
            return True
        else:
            return status

    def show(self):
        self.c.pipes["db"].send("SHOW")
        return True

    def refresh_ndb(self, ifnotdoneyet = False):
        if self.closed == True: return False
        self.logging.append("Triggered NameDB refresh...")
        if ifnotdoneyet == True and self.refreshed == True:
            return False

        self.c.pipes["live"].send("STOP")
        self.c.pipes["db"].send("STOP")
        refreshing = self.c.ndb.refresh()

        #refreshing usually takes a few seconds, so in this time we can do other tasks
        from time import ctime

        refreshing.join()
        self.c.pipes["live"].send("CONTINUE")
        self.c.pipes["db"].send("CONTINUE")
        self.logging.append("NameDB refresh complete.")
        self.refreshed = ctime()[4:-5]
        return True
