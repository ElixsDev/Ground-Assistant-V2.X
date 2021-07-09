def version():
    return "EliServices aprs component dbl.py at version 1.0\n"

class DBLogger:
    def __init__(self, **kwargs):
        try:
            from datetime import date

            global ct, ts, out, date, prc, name
            self._kill = False
            self.init = True

            ct = kwargs["ct"]
            ts = kwargs["ts"]
            out = kwargs["out"]
            date = date

            prc = kwargs["processGame"]()
            name = self.prc.prcname

        except:
            self.init = False
            return

        try:
            from ground_assistant.load import loadsql

        except:
            self.init = False
            prc.close()
            out.write(ct().split()[3] + ": dbl: ImportError while importing load.py.\n")
            return

        try:
            global db, dbc
            tables_one = loadsql(kwargs["sqlcred"][0], kwargs["sqlcred"][1])             #Calling loadsql function
            db = loadsql.db
            dbc = db.cursor()
            dbc.execute("SHOW TABLES;")
            row = list(dbc.fetchall())
            tables_two = [x for sublist in row for x in sublist]
            if tables_one != tables_two:                                                 #Make sure everything is okay
                raise Error
        except:
            self.init = False
            prc.close()
            out.write(ct().split()[3] + ": dbl: MySQLError while preparing db.\n")
            return


        db_prepare = self.preparesql()
        out.write(db_prepare[0])
        if db_prepare[1]:
            self.init = False
            out.write("dbl error: "+ db_prepare[1] + "\n")
            self.close()
            return

        out.write(ct().split()[3] + ": Component dbl started as: " + name + "\n")

    def run(self, dbl_pipe):
        while self._kill == False:
            beacon = dbl_pipe.recv()
            if beacon == "KILL":
                self._kill = True
                break

            out.write("dbl: " + beacon["address"] + "\n")

        self.close()
        return True

    def close(self):
        out.write(ct().split()[3] + ": Component dbl stopped as: " + name + "\n")
        out.flush()

        db.commit()
        db.close()

        prc.close()
        return True



    #Called after initalizing to prepare MySQL:
    def preparesql(self):
        #Create today's table...
        try:
            t_start = self.ts()                                                #First timestamp
            self.dbc = self.db.cursor()                                        #Create cursor() object to access MySQL
            x = {"CREATE TABLE IF NOT EXISTS " +                               #x is the SQL command to create a table,
                 str(self.date.today()).replace("-","_") +                     #where the name is todays date,
                 " ( time TIME," +                                             #First row is a timestamp,
                 " beacon_type VARCHAR(255)," +                                #second the type of beacon
                 " receiver VARCHAR(255)," +                                   #the receiver,
                 " device_id VARCHAR(6)," +                                    #FLARM ID,
                 " type VARCHAR(20)," +                                        #type of aircraft,
                 " north DOUBLE(180,7)," +                                     #coordinates north,
                 " east DOUBLE(180,7)," +                                      #coordinates south,
                 " groundspeed INT(255)," +                                    #groundspeed,
                 " msl INT(255)," +                                            #hight above sealevel (MSL),
                 " climbrate FLOAT(10)," +                                     #and the climbrate
                 " turnrate FLOAT(10)," +                                      #and the turnrate
                 " gps_horizontal FLOAT(10)," +                                #and the climbrate
                 " gps_vertical FLOAT(10));"}                                  #and the climbrate

            self.dbc.execute(''.join(list(x)))                                 #Execute the command
            return [self.ct().split()[3] + ": Created table in: " + str(round(self.ts() - t_start,2)) + "sec.\n", None]

        except Exception:
            return [self.ct().split()[3] + ": Failed to create todays table.\n", str(Exception)]

    #Called by the function that processes the beacon. Can be used without it, but needs preparesql() to be executed before.
    def dbw(self, beacon):
        #Build command...
        try:
            x = {"INSERT INTO " +                                              #This is the MySQL-comand that inserts our data in the database
                 str(self.date.today()).replace("-","_") +
                 " VALUES (" +
                 "\"" + str(beacon["timestamp"].time()) + "\"," +              #"\"" is just a masked " that is needed because SQL wants a string to be in "
                 "\"" + beacon["beacon_type"] + "\"," +
                 "\"" + beacon["receiver_name"] + "\"," +
                 "\"" + beacon["address"] + "\"," +
                 "\"" + str(beacon["aircraft_type"]) + "\"," +
                 str(round(beacon["latitude"],7)) + "," +                      #No strings, no masked "
                 str(round(beacon["longitude"],7)) + "," +
                 str(round(beacon["ground_speed"],2)) + "," +
                 str(round(beacon["altitude"],2)) + "," +
                 str(round(beacon["climb_rate"],2)) + "," +
                 str(round(beacon["turn_rate"],2)) + "," +
                 str(beacon["gps_quality"]["horizontal"]) + "," +
                 str(beacon["gps_quality"]["vertical"]) + ");"}

            self.dbc.execute(''.join(list(x)))                                 #Execute the command
            self.db.commit()
            return [self.ct().split()[3] + ": Beacon from: " + beacon["address"] + "\n", None]
        except:
            return [self.ct().split()[3] + ": Failed to write beacon to db.\n", str(Exception)]
