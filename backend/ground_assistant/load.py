#To understand this script, you need to know:
#    - Basic SQL syntax

#This script is responsible for loading the parameters.

#Load SQL:
def loadsql(sqluser,sqlpassword): #sqluser = Username for MySQL, sqlpassword = It's password
    import sys
    import mysql.connector as sql                                             #SQL-connector function

    #Connect to MySQL:
    try:
        loadsql.db=sql.connect(host="localhost", user=sqluser, passwd=sqlpassword)
        dbc = loadsql.db.cursor()
    except:
        sys.stderr.write("GA: Failed to connect to MySQL.\n")
        sys.exit()

    #Ensure database "ogn" is present:
    try:
        dbc.execute("SHOW DATABASES;")
        row = dbc.fetchall()
        row = [x for sublist in row for x in sublist]                         #Convert 2D list into 1D list
        try:
            isdb = row.index("ogn")
        except:
            dbc.execute("CREATE DATABASE ogn;")
            row = list(sqldb.fetchall())
    except:
        sys.stderr.write("GA: Failed to verify existence of database \"ogn\" at MySQL.\n")
        sys.exit()

    #Connect to database "ogn":
    try:
        dbc.execute("use ogn;")
        dbc.execute("show tables;")
        row = list(dbc.fetchall())
        row = [x for sublist in row for x in sublist]
    except:
        sys.stderr.write("GA: Failed to open database \"ogn\" at MySQL.\n")
        sys.exit()

    return row

#Load everything needed
def load(configpath="."):
    import os
    import sys

    #Loading configuration:
    try:                                                                      #Prevent code from crashing
        configpath = configpath + "/ga.conf"
        if os.path.exists(configpath):                                        #Make sure file is where its supposed to be
            configfile = open(configpath, "r")
            config = []
            for zeile in configfile:                                          #Write file content to variable
                x = zeile.strip()
                if x[:1] != "#":
                    config.append(x)

            if len(config) < 5:                                               #Prevents the rest of the code from crashing
                sys.stderr.write("GA: Missing parameters.\n")
                sys.exit()
            configfile.close()
        else:
            sys.stderr.write("GA: ga.conf not found.\n")
            sys.exit()
    except:
        sys.stderr.write("GA: Failed to load configuration\n")
        sys.exit()

    #Loading SQL:
    #try:
    #    lret = loadsql(config[9],config[10])                                   #Calling loadsql function
    #    dbc = loadsql.db.cursor()                                              #Transfer object
    #    dbc.execute("SHOW TABLES;")                                            #Test object
    #    row = list(dbc.fetchall())
    #    row = [x for sublist in row for x in sublist]
    #    if lret != row:                                                        #Make sure everything is okay
    #        nonsensetoraiseerror
    #except:
    #    sys.stderr.write("GA: Failed to load SQL.\n")
    #    sys.exit()

    #Return value(s):
    #load.db = loadsql.db                                                       #Make object available
    value = []
    value.append("")                                                           #Used to be an URL, but isn't needed in current versions
    value.append(config[7])                                                    #Runmode
    value.append(config[8])                                                    #Time to wait for main.collect
    coordinates = {"maxlat": b, "minlat": c, "maxlon": d, "minlon": e}
    value.append(coordinates)
    return value

def version():
    return "EliServices GA utility load.py at version 2.0\n"
