class PlaneHandler:
    def __init__(self, path):
        from ground_assistant.plugins.plane import NewPlane
        self.NewPlane = NewPlane
        self.airports = AirportHandler(path)
        self.index = {}

    def add(self, beacon):
        if beacon["address"] in self.index.keys(): self.index[beacon["address"]].update(beacon)
        else: self.index[beacon["address"]] = self.NewPlane(beacon, self.airports)
        return

    def clean(self, age = 5 * 60): #Age in seconds, default is 5 minutes
        for key in self.index.copy():
            if self.index[key].is_expired(age = age): self.index.remove(key)
        return

    def data(self, geo = "EDFM", alt = ["grounded", "landing", "nearby", "away"]):
        out = []
        for key in self.index:
            if (self.index[key].categorys["geo"] == geo and
                self.index[key].categorys["alt"] in alt and
                not self.index[key].is_expired()):

                out.append(self.index[key].relevant)

        return out

    def status(self):
        return "_status_:Nonfunctional"

    def datathread(self, pipe, flag, intervall, parameter, id, out = None):
        import json
        from time import sleep
        from os import devnull
        out = out if out else open(devnull, "a")

        out.write(f'(thread) {id}:online')
        while not flag.is_set():
            x = self.data(*parameter)
            x = json.dumps(x)
            pipe.send(f'{id}:{x}')
            sleep(intervall)
        out.write(f'(thread) {id}:offline')
        return

    def encode(parameter):
         if not parameter[0]: string = "____"
         else: string = parameter[0][:4]
         for i, item in enumerate(parameter[1]):
             string += item[:1]
         if i < 4: string += "".join(["_" for i in range(1, 4 - i)])
         return string

    def decode(code):
        if code[:4] != "____": parameter = [code[:4], []]
        else: parameter = [None, []]

        x = list(code[4:])
        for item in x:
            if item == "_": continue
            elif item == "g": parameter[1].append("grounded")
            elif item == "l": parameter[1].append("landing")
            elif item == "n": parameter[1].append("nearby")
            elif item == "a": parameter[1].append("away")
        return parameter

class AirportHandler:
    def __init__(self, path):
        from ground_assistant.common.load import ReadConfig
        file = ReadConfig(path, "airports.conf").getconfig("all")
        if file[0][:8] == "Default:":
            self.std_cat_alt = [int(x.strip()) for x in file[0][8:].split(",")]
            file.pop(0)
        else: raise InputError(f'Configfile corrupted, line 1 is {file[0][:8]}')

        self.airports = {}
        argcount = -1
        for line in file:
            if line[:1].isnumeric(): # -> No Airportname
                if argcount < 0: continue
                elif argcount < 4:
                    self.airports[current]["coordinates"].append(float(line.strip()[:-1]))
                    argcount +=1
                elif argcount == 4:
                    self.airports[current]["altitude"] = int(line.strip())
                    argcount += 1
                elif argcount > 4: continue
            else:
                current = line.strip()
                self.airports[current] = {"coordinates": [], "altitude": 0, "cat_alt": self.std_cat_alt}
                argcount = 0

    def find(self, coordinates, expected = None):
        if expected in self.airports.keys():
            x = {expected: self.airports.pop(expected)}
            x.update(self.airports)
            self.airports = x

        for port in self.airports:
            if (coordinates["latitude"] <= self.airports[port]["coordinates"][0] and
                coordinates["latitude"] >= self.airports[port]["coordinates"][1] and
                coordinates["longitude"] <= self.airports[port]["coordinates"][2] and
                coordinates["longitude"] >= self.airports[port]["coordinates"][3]):
                return [port, self.airports[port]]
        return
