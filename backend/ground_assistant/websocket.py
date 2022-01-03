certificate = '/home/elias/dev/ground-assistant/testunit/fullchain4.pem'
keyfile = '/home/elias/dev/ground-assistant/testunit/privkey4.pem'

import asyncio
import ssl
import websockets
import datetime

import logging
logger = logging.getLogger('websockets')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())


async def broadcast(message):
    websockets.broadcast(connected, message)

async def beacon_broadcast():
    while True:
        await asyncio.sleep(1)
        message = str(datetime.datetime.now())
        await broadcast(message)

async def collector(websocket):
    connected.add(websocket)
    await websocket.send("registered")
    try:
        async for _ in websocket:
            pass
    finally:
        await websocket.send("unregistered")
        connected.remove(websocket)

async def server():
    async with websockets.serve(collector, "", 5010, ssl=ssl_context):
        await beacon_broadcast()


ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain(certificate, keyfile = keyfile)
connected = set()
asyncio.run(server())
