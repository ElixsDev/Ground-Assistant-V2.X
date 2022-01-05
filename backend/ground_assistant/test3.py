mark = "test3"

def main(pipe, path):
    from setproctitle import setproctitle
    setproctitle("test3")

    keepalive = True
    while keepalive:
        beacon = pipe.recv()
        print(beacon)
        if beacon == "KILLtest3": keepalive = False
