mark = "plugin_stdout"

def main(pipe, path):
    from setproctitle import setproctitle
    setproctitle(mark)

    alive = True
    while alive:
        beacon = pipe.recv()
        print(beacon)
        if beacon == "KILLplugin_test": alive = False
