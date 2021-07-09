#The dblogger component logs the data of the aprs servers into MySQL.

class DBLogger:
    def __init__(self, db, out, processGame):
        #Importing...
        global ts, ct, sleep, dbc, date
        from datetime import date
        from time import ctime as ct, perf_counter as ts, sleep
        self._kill = False

        prepret = self.preparesql()
        try:
            prep = prepret.result
        except:
            prep = prepret.error

        out.write(ct().split()[3] + " component dblogger started as: " + name + "\n" + prep)

    #Called after initalizing to prepare MySQL:
    def preparesql(self):
        #Create today's table...
        try:
            t_start = ts()                                                     #First timestamp
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
        #Build command...
        x = {"INSERT INTO " +                                                  #This is the MySQL-comand that inserts our data in the database
            str(date.today()).replace("-","_") +
                " VALUES (" +
                "\"" + str(beacon["timestamp"].time()) + "\"," +               #"\"" is just a masked " that is needed because SQL wants a string to be in "
                "\"" + beacon["beacon_type"] + "\"," +
                "\"" + beacon["receiver_name"] + "\"," +
                "\"" + beacon["address"] + "\"," +
                "\"" + str(beacon["aircraft_type"]) + "\"," +
                "\"None\"," +                                                  #short       ??
                "\"None\"," +                                                  #callsign    ??
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

    def run(self, dbl_pipe):
        

    def close(self):
        if self._kill == False:
            self._kill = True
            db.commit()
            db.close()

            out.write(ct().split()[3] + ": component dblogger stopped as: " + name + "\n")
            out.flush()
            return True
        else:
            return False

    #Prints version.
    def version(self):
        self.result = "EliServices GA utility dblogger.py at version 1.0\n"
        return
