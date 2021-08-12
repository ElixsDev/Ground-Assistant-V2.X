#This is the main file for logging data of the aprs servers.
#It replaces the now outdated versions 1.x.x of ground_assistant.main, ground_assistant.data and ground_assistant.utils.

class aprs_logger:
    def __init__(self,path):
        #Importing...
        import sys
        global ts, ct, sleep, config, aprs_error, executed
        from time import ctime as ct, perf_counter as ts, sleep
        t_start = ts()                                                         #First timestamp
        executed = False
        self._kill = False

        try:
            global parse                                                       #Only parse is needed globaly here
            from ogn.client import AprsClient                                  #Import the aprs packages
            from ogn.parser import parse, ParseError
        except:
            self.error = "aprs: Package \"ogn-client\" missing.\n"               #You need to check for the existance of this variable after the execution, there won't be a python error.
            return


        try:
            from ground_assistant.load import load                             #Import internal librarys
        except:
            self.error = "aprs: Internal library error.\n"
            return


        #Configuring...
        try:
            config = load(path)                                                #Settings are beeing loaded from configfile and MySQL is beeing prepared
            self.config = config                                               #Make configs available

            if config[1] == "console":                                         #Redirect output to console
                self.out = sys.stderr
                aprs_error = sys.stderr
            elif config[1] == "logfile":                                       #Redirect output to logfile
                self.out = open(path + "/ga.log", "a")
                aprs_error = open(path + "/aprs_error.log", "a")               #File where ogn-client errors are beeing logged
            else:                                                              #No output, but still write method (makes it easier)
                self.out = open("/dev/null", "a")
                aprs_error = open("/dev/null", "a")

        except Exception as er:                                                #Since errors can get complicated here, the original error is included here
            self.error = "aprs: Error while loading:" + str(er) + "\n"
            return

        try:
            self.client = AprsClient(aprs_user='N0CALL')                       #Connecting to APRS-Servers
            self.client.connect()

        except Exception as er:                                                #Also many different possible failures, so error is included
            self.error = "aprs: Can't connect to APRS server." + str(er) + "\n"
            return

        self.result = "\n" + ct().split()[3] + " EliServices Ground Assistant Library started.\nLoading done in: " + str(round(ts() - t_start,2)) + "sec.\n"

    def rtd_process(self, rtd_pipe_recv):
        from ground_assistant.rtd import RealTimeData
        rtd = RealTimeData(ct, self.out, self.processGame)
        rtd.run(rtd_pipe_recv)

    def dbl_process(self, dbl_pipe_recv):
        from ground_assistant.dbl import DBLogger
        parameter = {"ct": ct, "ts": ts, "out": self.out, "processGame": self.processGame, "sqlcred": [self.config[9], self.config[10]]}
        dbl = DBLogger(**parameter)
        if dbl.init == True:
            dbl.run(dbl_pipe_recv)

    def create_listener(self, processGame):
        global rtd_pipe_recv, rtd_pipe_send, rtd_p, dbl_pipe_recv, dbl_pipe_send, dbl_p
        self.processGame = processGame
        from multiprocessing import Process, Pipe

        rtd_pipe_recv, rtd_pipe_send = Pipe()
        rtd_p = Process(target=self.rtd_process, args=(rtd_pipe_recv, ))
        rtd_p.start()

        dbl_pipe_recv, dbl_pipe_send = Pipe()
        dbl_p = Process(target=self.dbl_process, args=(dbl_pipe_recv, ))
        dbl_p.start()
        return [rtd_p, dbl_p]

    #This function processes the beacon. It needs preparesql() to be executed before.
    def process_beacon(self,raw_message):
        #Trying to parse the beacon with the "ogn-client" library parser...
        if self._kill != False: return

        try:
            beacon = parse(raw_message)
        except Exception as er:
            aprs_error.write(str(er) + "\n")                             #Failures are written to a seperate file to monitore them
            aprs_error.flush()
            return

        #Filter the beacons and hand them to the processes
        try:
            if beacon["aprs_type"] == "position" and beacon["beacon_type"] == "flarm" and float(beacon["latitude"]) <= float(config[3]["maxlat"]) and float(beacon["latitude"]) >= float(config[3]["minlat"]):
                if float(beacon["longitude"]) <= float(config[3]["maxlon"]) and float(beacon["longitude"]) >= float(config[3]["minlon"]):
                    rtd_pipe_send.send(beacon)
                    dbl_pipe_send.send(beacon)
            return [None]

        except Exception:
            return [Exception]

    def close(self):
        if executed != False: return
        self.out.write("aprs.close: called...\n")
        executed = True
        self._kill = True
        sleep(1)
        self.client.disconnect()

        try:
            rtd_pipe_send.send("KILL")
            dbl_pipe_send.send("KILL")
            sleep(1)
        except Exception:
            self.out.write("aprs.close: unable to send kill command over pipes.\n")

        self.out.write("aprs.close: child processes...\n")
        if dbl_p.is_alive():
            self.out.write("DBL is alive!\n")
            dbl_p.terminate()
        #dbl_p.close()

        if rtd_p.is_alive():
            self.out.write("RTD is alive!\n")
            rtd_p.terminate()
        #rtd_p.close()

        #self.out.write("aprs.close: MySQL...\n")
        #db.commit()
        #db.close()

        self.out.write("aprs.close: aprs_error file...\n")
        aprs_error.flush()
        aprs_error.close()

        self.out.write(ct().split()[3] + ": Exiting.\n")
        self.out.flush()
        return True

    #Prints version.
    def version(self):
        from ground_assistant.rtd import version as rtd_version
        from ground_assistant.dbl import version as dbl_version
        return "EliServices GA utility aprs.py at version 2.1\n" + rtd_version() + dbl_version()
