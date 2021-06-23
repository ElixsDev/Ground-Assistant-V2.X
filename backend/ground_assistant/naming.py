#Version: 1.0, Copyright: EliServices

class NameDB:
    def __init__(self):
        global os, ctime, log, config, db
        import os
        from time import ctime
        from ground_assistant.load import load

        path = os.path.abspath(".")

        config = load(path)                                                #Settings are beeing loaded from configfile and MySQL is beeing prepared
        db = load.db                                                       #Transfer sql object

        if config[1] == "console":                                         #Redirect output to console
            log = sys.stderr
        elif config[1] == "logfile":                                       #Redirect output to logfile
            log = open(path + "/NameDB.log", "a")
        else:                                                              #No output, but still write method (makes it easier)
            log = open("/dev/null", "a")

        log.write(ctime().split()[3] + ": Started: Success.\n")
        log.flush()

    def refresh(self):
        log.write(ctime().split()[3] + ": Refreshing...\n")
        log.flush()

        log.write(ctime().split()[3] + ": Refreshing: Success.\n")
        log.flush()
        return

    def identify(self):
        return

    def close(self):
        log.write(ctime().split()[3] + ": Exiting: Success.\n")
        log.flush()
        log.close()                                                                                   #Close logfile
        return
