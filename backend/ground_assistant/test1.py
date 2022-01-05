mark = "test1"

def main(pipe, path):
    from setproctitle import setproctitle
    setproctitle(mark)

    keepalive = True
    while keepalive:
        beacon = pipe.recv()
        print(beacon)
        if beacon == "KILLtest1": keepalive = False
