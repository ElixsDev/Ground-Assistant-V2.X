def version():
    return "EliServices aprs component rtd.py at version 1.0\n"

class RealTimeData:
    def __init__(self, ct, out, processGame):
        self._kill = False

        self.ct = ct
        self.out = out

        self.prc = processGame()
        self.name = self.prc.prcname

        self.out.write(self.ct().split()[3] + ": Component rtd started as: " + self.name + "\n")

    def run(self, rtd_pipe):
        while self._kill == False:
            beacon = rtd_pipe.recv()
            if beacon == "KILL":
                self._kill = True
                break

            self.out.write("rtd: " + beacon["address"] + "\n")

        self.close()
        return True

    def close(self):
        self.out.write(self.ct().split()[3] + ": Component rtd stopped as: " + self.name + "\n")
        self.out.flush()
        self.prc.close()
        return True
