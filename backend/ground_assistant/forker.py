class TheFork:
    def __init__(self, path, pipe):
        import os
        from multiprocessing import Process

        self.Process = Process
        self.path = path
        self.pipe = pipe
        self.plugins = {}
        self.pool = {}

        self.memorypath = path + "/thefork.conf"
        if os.path.exists(self.memorypath):
            memory = open(self.memorypath, "r")
            for line in memory:
                x = line.strip()
                if x[:1] != "#":
                    try:
                        exec(f'import {x} as np\nself.plugins["{x}"] = np\n')
                    except:
                        pass

            memory.close()

        self.memory = open(self.memorypath, "a")

    def register(self, id):
        reserved_keys = ["all"]
        if id in reserved_keys: return f'{id} is not a valid PlugIn name'

        try:
            exec(f'import {id} as np\nif np.mark != "{id}": raise AttributeError\nself.plugins["{id}"] = np')

        except ImportError as ie:
            return str(ie)
        except AttributeError as ae:
            return "PlugIn is not valid"

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

    def load(self, id):
        if id == "all":
            for item in self.plugins:
                if item in self.pool: continue
                self.pool[item] = self.Process(target=self.plugins[item].main, args=(self.pipe["receive"], self.path,))
                self.pool[item].start()
            return "loaded all"

        if not id in self.plugins: return f'{id} is not registered'
        if id in self.pool: return f'{id} is loaded'

        self.pool[id] = self.Process(target=self.plugins[id].main, args=(self.pipe["receive"], self.path,))
        self.pool[id].start()
        return f'loaded {id}'

    def restart(self, id):
        if not id in self.pool and id != "all": return f'{id} is not loaded'
        self.close(id)
        self.load(id)
        return f'restarted {id}'

    def close(self, id):
        if len(self.pool) == 0: return f'closed {id}'
        if id == "all":
            try:
                self.pipe["send"].send(f'KILLALL')
            except:
                pass
            else:
                for item in self.pool:
                    self.pool[item].join()
            finally:
                for item in self.pool:
                    self.pool[item].close()

                self.pool.clear()
                return "closed all"

        if not id in self.pool: return f'{id} is not loaded'
        try:
            self.pipe["send"].send(f'KILL{id}')
        except:
            pass
        else:
            self.pool[id].join()
        finally:
            self.pool[id].close()
            self.pool.pop(id)
            return f'closed {id}'

    def end(self):
        self.close("all")
        self.memory.flush()
        self.memory.close()
        return "Ended."
