#Receives Data from ogn Network

mark = "" #Prevents from beeing registered as normal plugin

class Receiver():
    def __init__(self, pipe, path):
        self.path = path
        self.pipe = pipe

    def init(self):
        try:
            from ogn.client import AprsClient
            from ogn.parser import parse, ParseError

        except ImportError:
            self.crashreport = "Failed to import ogn-package"
            return False

        from multiprocessing import Process
        self.parse = parse
        self.client = AprsClient(aprs_user='N0CALL')

        try:
            self.client.connect()
            self.receiver = Process(target=self.client.run, kwargs={"callback": self.scream,
                                                                "autoreconnect": True,})
            self.is_alive = self.receiver.is_alive
            return True
        except Exception as ex:
            self.crashreport = [ex, self.testsocket()]
            self.close()
            return False

    def scream(self, raw_message):
        try:
            beacon = self.parse(raw_message)
        except Exception as message:
            #self.log(str(message))
            return

        if (beacon["aprs_type"] == "position" and
            beacon["beacon_type"] == "flarm" and
            beacon["aircraft_type"] == 1):
            self.pipe.send(beacon)
        return

    def run(self):
        self.receiver.start()
        return

    def close(self):
        self.client.disconnect()
        self.receiver.kill()
        self.receiver.join()
        self.receiver.close()
        return

    def testsocket(self):
        import socket
        from ogn.client import settings
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        sock.settimeout(5)
        sock.connect((settings.APRS_SERVER_HOST, settings.APRS_SERVER_PORT_CLIENT_DEFINED_FILTERS))
        ret = sock
        sock.close()
        return ret
