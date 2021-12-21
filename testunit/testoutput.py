from time import sleep
from multiprocessing.connection import Client
from ground_assistant.load import ReadConfig
configs = ReadConfig("/home/elias/dev/ground-assistant/daemon")
li = configs.getconfig("li")

geo = "EDFM"
args = [{"geocat": geo, "altcat": "grounded"},{"geocat": geo, "altcat": "landing"},{"geocat": geo, "altcat": "nearby"},{"geocat": geo, "altcat": "away"}]
out = {}

for item in args:
    client = Client(('localhost', li["port"]), authkey=li["password"].encode('utf-8'))
    client.send(item)
    out[item["altcat"]] = client.recv()
    client.close()
    sleep(1)

print(out)
