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
