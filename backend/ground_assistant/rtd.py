class RealTimeData:
    def __init__(self):
        global sys
        import sys
        sys.stderr.write("Activated!\n")

    def run(self):
        sys.stdout.write("I am running...\n")

    def kill(self):
        sys.stdout.write("I was killed!")
