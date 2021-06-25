#This is the main file for logging data of the aprs servers.
#It replaces the now outdated versions 1.x.x of ground_assistant.main, ground_assistant.data and ground_assistant.utils.

class aprs_logger:
    def __init__(self,path):
        #Importing...
        import sys
        global ts, ct, db, aprs_error, config
        from time import ctime as ct, perf_counter as ts
        t_start = ts()                                                         #First timestamp
        self._kill = False

        try:
            global parse                                                       #Only parse is needed globaly here
            from ogn.client import AprsClient                                  #Import the aprs packages
            from ogn.parser import parse, ParseError

        except:
            self.error = "GA: Package \"ogn-client\" missing.\n"               #You need to check for the existance of this variable after the execution, there won't be a python error.
            return


        try:
            from ground_assistant.load import load                             #Import internal librarys

        except:
            self.error = "GA: Internal library error.\n"
            return


        #Configuring...
        try:
            config = load(path)                                                #Settings are beeing loaded from configfile and MySQL is beeing prepared
            self.config = config

            db = load.db                                                       #Transfer sql object

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
            self.error = "GA: Error while loading:" + str(er) + "\n"
            return

        try:
            self.client = AprsClient(aprs_user='N0CALL')                       #Connecting to APRS-Servers
            self.client.connect()

        except Exception as er:                                                #Also many different possible failures, so error is included
            self.error = "GA: Can't connect to APRS server." + str(er) + "\n"
            return

        self.result = "\n" + ct().split()[3] + " EliServices Ground Assistant Library started.\nLoading done in: " + str(round(ts() - t_start,2)) + "sec.\n"

    #Called after initalizing to prepare MySQL:
    def preparesql(self):
        from datetime import date

        #Create today's table...
        try:
            t_start = ts()                                                     #First timestamp
            global dbc
            dbc = db.cursor()                                                  #Create cursor() object to acces MySQL
            x = {"CREATE TABLE IF NOT EXISTS " +                               #x is the SQL command to create a table
                 str(date.today()).replace("-","_") +                          #where the name is todays date
                 " ( time TIME," +                                             #First row is a timestamp,
                 " beacon_type VARCHAR(255)," +                                #second the type of beacon
                 " receiver VARCHAR(255)," +                                   #the receiver,
                 " device_id VARCHAR(6)," +                                    #FLARM ID,
                 " type VARCHAR(20)," +                                        #type of aircraft,
                 " short VARCHAR(10)," +                                       #Quickly identify aircrafts,
                 " callsign VARCHAR(10)," +                                    #official callsign,
                 " north DOUBLE(180,7)," +                                     #coordinates north,
                 " east DOUBLE(180,7)," +                                      #coordinates south,
                 " groundspeed INT(255)," +                                    #groundspeed,
                 " msl INT(255)," +                                            #hight above sealevel (MSL),
                 " climbrate FLOAT(10)," +                                     #and the climbrate
                 " turnrate FLOAT(10)," +                                      #and the turnrate
                 " gps_horizontal FLOAT(10)," +                                #and the climbrate
                 " gps_vertical FLOAT(10));"}                                  #and the climbrate

            dbc.execute(''.join(list(x)))                                      #Execute the command

            try:                                                               #Sometimes for some reason this gives an error
                row = list(dbc.fetchall())                                     #Read SQL's reaction (=> 2D list)
                row = [x for sublist in row for x in sublist]                  #This makes the 2D list row 1D
            except:                                                            #The lines aren't needed, we can continue as usual
                pass

            self.result = "Created table in: " + str(round(ts() - t_start,2)) + "sec.\n"
            return

        except Exception as er:
            self.error = "GA: Failed to create today's table." + str(er) + "\n"
            return

    #Called by the function that processes the beacon. Can be used without it, but needs preparesql() to be executed before.
    def dbw(self,beacon):
        from datetime import date

        #Build command...
        x = {"INSERT INTO " +                                                  #This is the MySQL-comand that inserts our data in the database
            str(date.today()).replace("-","_") +
                " VALUES (" +
                "\"" + str(beacon["timestamp"].time()) + "\"," +               #"\"" is just a masked " that is needed because SQL wants a string to be in "
                "\"" + beacon["beacon_type"] + "\"," +
                "\"" + beacon["receiver_name"] + "\"," +
                "\"" + beacon["address"] + "\"," +
                "\"" + str(beacon["aircraft_type"]) + "\"," +
                "\"" + beacon["name"] + "\"," +                                #short       ??
                "\"" + beacon["dstcall"] + "\"," +                             #callsign    ??
                str(round(beacon["latitude"],7)) + "," +                       #No strings, no masked "
                str(round(beacon["longitude"],7)) + "," +
                str(round(beacon["ground_speed"],2)) + "," +
                str(round(beacon["altitude"],2)) + "," +
                str(round(beacon["climb_rate"],2)) + "," +
                str(round(beacon["turn_rate"],2)) + "," +
                str(beacon["gps_quality"]["horizontal"]) + "," +
                str(beacon["gps_quality"]["vertical"]) + ");"}

        content = (''.join(list(x)))                                           #Converts 2D list in string
        dbc.execute(content)                                                   #Execute SQL command content[i]
        db.commit()
        return "Executed: " + content                                          #Other than the functions for initialisation, this directly returns its success message

    #This function processes the beacon. It needs preparesql() to be executed before.
    def process_beacon(self,raw_message):
        #Trying to parse the beacon with the "ogn-client" library parser...
        if self._kill != False:
            self._kill = None
            return

        try:
            beacon = parse(raw_message)

        except Exception as er:
            aprs_error.write(str(er) + "\n")                                   #Failures are written to a seperate file to monitore them
            aprs_error.flush()
            return

        #Write the right beacons into the database...
        try:
            if beacon["aprs_type"] == "position" and beacon["beacon_type"] == "flarm" and float(beacon["latitude"]) <= float(config[3]["maxlat"]) and float(beacon["latitude"]) >= float(config[3]["minlat"]):
                if float(beacon["longitude"]) <= float(config[3]["maxlon"]) and float(beacon["longitude"]) >= float(config[3]["minlon"]):
                    #If the beacons meet the requirements (beeing a flarm beacon inside the defined square), it will get written...
                    self.out.write(self.dbw(beacon) + "\n")
                    if config[1] == "logfile": self.out.flush()

        except Exception as er:
            self.error = er                                                    #Errors are to complicated here
            return

        return

    def close(self):
        if self._kill == False:
            from time import sleep
            self._kill = True
            sleep(1)
            self.client.disconnect()

            sleep(1)
            db.close()

            aprs_error.flush()
            aprs_error.close()

            self.out.write("\n" + ct().split()[3] + " EliServices Ground Assistant Library exited.\n")
            self.out.flush()
            return True

        return False

    #Prints version.
    def version(self):
        self.result = "EliServices GA utility aprs.py at version 2.0\n"
        return
