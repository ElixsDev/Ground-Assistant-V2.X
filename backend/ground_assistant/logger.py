from ground_assistant.errorhandlers import *

class Logger:
    def __init__(self, **kwargs):
        from time import ctime as ct
        global ct

        runmode = kwargs["config_obj"].getconfig("runmode")
        if runmode == "console":
            from sys import stderr
            self.out = stderr
        elif runmode == "logfile":
            from os.path import exists
            path = kwargs["path"] + "/logs/"
            if not exists(path):
                from os import mkdir
                mkdir(path)
            self.out = open(path + kwargs["name"], "a")
        else:
            self.out = open("/dev/null", "a")

    def append(self, message):
        self.out.write(ct()[4:-5] + ": " + str(message) + "\n")
        self.out.flush()
        return True

    def close(self):
        self.out.flush()
        self.out.close()
        return True
