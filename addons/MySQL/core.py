class SQLAnalyzer:
    def __init__(self, path, dat = "2021_10_24"):
        from datetime import date
        self.date = str(date.today()).replace("-","_")
        self.date = dat

        from ground_assistant.load import ReadConfig, mySQL
        from ground_assistant.logger import Logger
        self.configs = ReadConfig(path)
        self.mysql = mySQL()
        self.logging = Logger(config_obj = self.configs, path = path, name = "sqlanalyzer.log")

        self.ids = self.mysql.sendquery("SELECT device_id FROM " + self.date + " GROUP BY device_id;")

        result = self.mysql.sendquery("SELECT * FROM sfvm_planes;")

        temp = []
        self.relevant_planes = []
        self.was_online = {}
        self.relevant_data = {}

        i = 0
        for item in result:
            i += 1
            temp.append(item)
            if i == 7:
                self.relevant_planes.append(temp)
                temp = []
                i = 0

        for item in self.relevant_planes:
            try:
                self.ids.index(item[1])
                self.was_online[item[1]] = [item[3], item[4], item[2]]
            except ValueError:
                pass

        self.test()

    def get_relevant_data(self):
        for key in self.was_online:
            res = self.mysql.sendquery("SELECT * FROM " + self.date + " WHERE device_id = \"" + key + "\" ORDER BY time;")
            self.relevant_data[key] = self.mysql.multiline
            #print("Got data.")
        return

    def get_flights(self):
        #ground = self.configs.getconfig("coordinates")["altitude"] + 5
        self.flights = {}
        for key in self.relevant_data:
            self.key = key
            self.flights[key] = []
            self.flight = []
            self.flightinfo = [0, 0] #Max height, time
            self.current = False
            self.newplane = True
            for data in self.relevant_data[key]:
                self.process_data(data)

        return

    def process_data(self, data):
        if data[7] > 0:
            if self.current == False and self.newplane == False:
                self.flightinfo[1] = self.olddata[0]
                self.flight.append(self.olddata)
                #print("speed: ", self.olddata[7], " height: ", self.olddata[8])
                self.current = True

            if self.newplane == True: self.newplane = False
            if data[8] > self.flightinfo[0]: self.flightinfo[0] = data[8]
            self.flight.append(data)
            #print("speed: ", data[7], " height: ", data[8])

        elif data[7] <= 0:
            if self.current == True:
                self.flightinfo[1] = data[0] - self.flightinfo[1]
                self.flight.append(data)
                #print("speed: ", data[7], " height: ", data[8])
                self.flights[self.key].append([self.flightinfo, self.flight])
                print(self.flightinfo)
                if self.flightinfo[0] == 98:
                    print(self.flight)
                self.flight = []
                self.flightinfo = [0,0]
                self.current = False
                #print("-          -")

        if self.current == False: self.olddata = data
        return

    def test(self):
        self.get_relevant_data()
        self.get_flights()
        return self.flights

#SQLAnalyzer("/home/elias/dev/ground-assistant/daemon")
