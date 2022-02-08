class Web_Socket():
    def __init__(self, path, pipe_in, flag, status, get_cat, out = None):
        global asyncio
        global websockets

        import asyncio
        import websockets
        import ssl
        from os import devnull

        self.out = out if out else open(devnull, "a")
        self.pipe_in = pipe_in
        self.kill = flag
        self.connected = set()
        self.status = status
        self.get_cat = get_cat

        #import logging
        #logger = logging.getLogger('websockets')
        #logger.setLevel(logging.INFO)
        #logger.addHandler(logging.StreamHandler())

        certificate = f'{path}/fullchain4.pem'
        keyfile = f'{path}/privkey4.pem'
        self.ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        self.ssl_context.load_cert_chain(certificate, keyfile = keyfile)

    async def broadcast(self, message):
        self.out.write(f'(broadcast) {message}\n')
        self.out.flush()
        websockets.broadcast(self.connected, message)
        return

    async def beacon_broadcast(self):
        while not self.kill.is_set():
            await asyncio.sleep(1)
            beacon = self.pipe_in.recv()
            await self.broadcast(beacon)
        return

    async def collector(self, websocket):
        self.connected.add(websocket)
        await websocket.send("registered")
        self.get_cat(await websocket.recv())
        await websocket.send(self.status())
        self.out.write(f'(connection) {websocket}\n')
        self.out.flush()
        try:
            async for _ in websocket:
                pass
        finally:
            await websocket.send("unregistered")
            self.connected.remove(websocket)
            self.out.write("(connection) closed\n")
            self.out.flush()
        return

    async def server(self):
        async with websockets.serve(self.collector, "", 5010, ssl=self.ssl_context):
            await self.beacon_broadcast()
        return

    def run(self):
        self.out.write("(info) websocket started\n")
        self.out.flush()
        asyncio.run(self.server())
        self.out.write("(info) websocket closed\n")
        self.out.flush()
        return
