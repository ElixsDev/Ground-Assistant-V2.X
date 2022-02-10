class TheFork:
    def __init__(self, path, receive = True, load = True, ndb_refresh = True, out = None):
        import os
        from multiprocessing import Process, Pipe
        from threading import Thread, Event
        from importlib import reload, invalidate_caches
        from ground_assistant import namedb

        if out == None: out = open(os.devnull, 'a')
        out.write("Startup\n")

        self.Process = Process
        self.Pipe = Pipe
        self.recache = invalidate_caches
        self.reload_mod = reload #self.reload is a function in this file
        self.path = path
        self.out = out
        self.pipe_in, self.pipe_out = Pipe()

        self.plugins = {}
        self.pool = {}
        self.pipes = {}

        self.dstthread = Thread(target=self.distr_center, name="DistributionCenter")
        self.kill = Event()
        self.dstthread.start()

        self.memorypath = path + "/thefork.conf"
        if os.path.exists(self.memorypath):
            memory = open(self.memorypath, "r")
            for line in memory:
                x = line.strip()
                if x[:1] != "#":
                    try:
                        exec(f'from ground_assistant.plugins import {x} as np\nself.plugins["{x}"] = np\n')
                    except:
                        pass

            memory.close()
        self.memory = open(self.memorypath, "a")
        self.ndb = namedb.NameDB()
        if ndb_refresh: self.ndb.refresh_ndb()
        if receive: self.load_receiver()
        if load: self.loadall()

#Handling of Data-Output:
    #Thread
    def distr_center(self):
        while not self.kill.is_set():
            beacon = self.pipe_in.recv()
            try:
                for item in self.pipes:
                    try:
                        self.pipes[item].send(beacon)
                    except BrokenPipeError:
                        self.out.write(f'Catched BrokenPipeError for {item}\n')
                        self.close(item)
            except RuntimeError as error:
                 self.out.write(f'Catched RuntimeError: {error}\n')
        return

    def register(self, id):
        reserved_keys = ["all", "distr_center", "main"]
        if id in reserved_keys: return f'{id} is not a valid PlugIn name'
        try:
            self.recache()
            exec(f'import ground_assistant.plugins.{id} as np\n'
               + f'if np.mark != "{id}": raise AttributeError(np.mark + " != {id}")\n'
               + f'self.plugins["{id}"] = np')

        except ImportError as ie:
            return str(ie)
        except AttributeError as ae:
            return f'PlugIn is not valid (ae)'

        else:
            self.memory.write(id + "\n")
            self.memory.flush()
            return f'registered {id}'

    def remove(self, id):
        if not id in self.plugins: return f'{id} is not registered'
        self.close(id)
        self.plugins.pop(id)

        memorydel = open(self.memorypath, "r")
        lines = memorydel.readlines()
        memorydel.close()

        hangover = ""
        memorydel = open(self.memorypath, "w")
        for line in lines:
            if line.strip("\n") != id: memorydel.write(line)
            else: hangover += "\n"
        memorydel.write(hangover)
        memorydel.close()

        return f'removed {id}'

    def reload(self, ids):
        ids = [ids]
        if not ids[0] in self.plugins and ids[0] != "all" : return f'{ids[0]} is not registered'
        if ids[0] == "all": ids = self.plugins

        for item in ids:
            self.close(item)
            self.plugins[item] = self.reload_mod(self.plugins[item])
            self.load(item)
        return f'reloaded {ids}'

    def load(self, ids):
        ids = [ids]
        if not ids[0] in self.plugins and ids[0] != "all" : return f'{ids[0]} is not registered'
        if ids[0] == "all": ids = self.plugins

        for item in ids:
            if item in self.pool: continue
            p_recv, p_send = self.Pipe()
            self.pool[item] = self.Process(target = self.plugins[item].main,
                                           args = (p_recv, self.path, ndb = self.ndb.getname))
            self.pool[item].start()
            self.pipes[item] = p_send
        return f'loaded {ids}'

    def restart(self, id):
        if not id in self.pool and id != "all": return f'{id} is not loaded'
        self.close(id)
        self.load(id)
        return f'restarted {id}'

    def close(self, ids):
        if len(self.pool) == 0: return f'closed {id}'

        if ids == "all": ids = list(self.pool.keys())
        if type(ids) == str: ids = [ids]

        for item in ids:
            if not item in self.pool:
                ids = f'none, {ids[0]} is not loaded'
                continue

            try:
                self.pipe_out.send(f'KILL{item}')
            except:
                pass
            else:
                self.pool[item].join()
            finally:
                self.pipes.pop(item)
                self.pool[item].close()
                self.pool.pop(item)
        return f'closed {ids}'

    #Shortcuts:
    def loadall(self):
        return self.load("all")

    def reloadall(self):
        return self.reload("all")

    def restartall(self):
        return self.restart("all")

    def closeall(self):
        return self.close("all")


#Handling of Data-Input:
    def load_receiver(self, simulated = False):
        if simulated:
            from ground_assistant.plugins.simulator import Receiver, TestHelper
            self.helper = TestHelper
        else: from ground_assistant.plugins.receiver import Receiver

        self.receiver = Receiver(self.pipe_out, self.path)
        if not self.receiver.init(): return self.receiver.crashreport
        self.receiver.run()
        return "Receiver loaded"

    def close_receiver(self):
        try:
            self.receiver.close()
            return "Receiver closed"
        except AttributeError:
            return "Receiver not loaded"

    def reload_receiver(self, simulated = False):
        self.close_receiver()
        self.load_receiver(simulated)
        return "Receiver reloaded"

#Generall:
    def end(self):
        try: self.close_receiver()
        except Exception as ex: self.out.write(f'{str(ex)}\n')

        try: self.closeall()
        except Exception as ex: self.out.write(f'{str(ex)}\n')

        self.kill.set()
        self.pipe_out.send("") #If there are no incomming beacons, the loop won't check the event
        if self.dstthread.is_alive(): self.dstthread.join(5)
        if self.dstthread.is_alive(): self.out.write("failed joining thread\n")

        w = 0
        if self.ndb.refreshprc.is_alive(): self.out.write("Waiting for ndb refresher")
        while self.ndb.refreshprc.is_alive():
            w += 1
            self.out.write(".")
            self.sleep(1)
            if w > 10: self.ndb.refreshprc.kill()
        self.out.write("\n")
        self.ndb.close()

        self.memory.flush()
        self.memory.close()
        self.out.write("Ended\n")
        self.out.flush()
        self.out.close()
        return "ended"

def version():
    return "forker.py: 1.0"
