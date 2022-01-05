mark = "test2"

def main(pipe, path):
    from setproctitle import setproctitle
    setproctitle("test2")

    keepalive = True
    while keepalive:
        beacon = pipe.recv()
        print(beacon)
        if beacon == "KILLtest2": keepalive = False
