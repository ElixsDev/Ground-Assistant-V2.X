from ground_assistant.errorhandlers import *

class Logger:
    def __init__(self,**kwargs):
        from time import ctime as ct
        global ct

        runmode = kwargs["config_obj"].getconfig("runmode")
        if runmode == "console":
            from sys import stderr
            self.out = stderr
        elif runmode == "logfile":
            self.out = open(kwargs["path"] + "/ga.log", "a")
        else:
            self.out = open("/dev/null", "a")

    def append(self, message):
        self.out.write(ct()[4:-5] + ": " + message + "\n")

    def close(self):
        self.out.flush()
        self.out.close()
