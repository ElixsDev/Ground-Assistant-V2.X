mark = "plugin_live"

def main(pipe, path, ndb):
    from setproctitle import setproctitle
    setproctitle(mark)

    from sys import stdout, stderr
    from threading import Thread, Event
    from multiprocessing import Pipe
    from ground_assistant.plugins.web_socket import Web_Socket
    from ground_assistant.plugins.planehandler import PlaneHandler

    keepalive = True
    wait = False
    p_recv, p_send = Pipe()
    flag = Event()
    handler = PlaneHandler(path, ndb)
    openthreads = {}

    def get_cat(code):
        got_parameter = PlaneHandler.decode(code)
        if not code in openthreads.keys():
            #optionally add stdout to get some info
            openthreads[code] = Thread(target=handler.datathread, args=(p_send, flag, 1, got_parameter, code), name = code)
            openthreads[code].start()
        return

    def radar(p_send):              #The Websocket awaits a brodacastet message,
        from time import sleep      #so you cant connect without a message beeing broadcastet
        while len(openthreads) < 1:
             p_send.send("Echo")
             sleep(1)
        return

    serverobj = Web_Socket(path, p_recv, flag, handler.status, get_cat) #optionally add stdout to get some info
    serverthread = Thread(target=serverobj.run, name = "WebSocket")
    serverthread.start()

    radarthread = Thread(target=radar, args=(p_send,), name = "Radar")
    radarthread.start()
    init = True

    while keepalive:
        beacon = pipe.recv()
        if isinstance(beacon, str):
            if beacon[:4] == "KILL":
                if beacon[4:] == mark:
                    keepalive = False
                    break
                else:
                    continue

            elif beacon == "STOP":
                wait = True
                continue
            elif beacon == "CONTINUE":
                wait = False
                continue

        if init == False: continue
        handler.add(beacon)

    if init == True:
        flag.set()
        p_send.send("PingPong")
        serverthread.join()
        for item in openthreads: openthreads[item].join()
        openthreads["Trigger"] = "Trigger" #In case no thread was spawned
        radarthread.join()
        return
