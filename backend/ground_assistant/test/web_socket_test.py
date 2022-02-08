from multiprocessing import Pipe
p_recv, p_send = Pipe()
import sys, threading
path = "/home/elias/dev/ground-assistant/daemon"
flag = threading.Event()
#flag.set()
out = sys.stdout
from ground_assistant.plugins.web_socket import Web_Socket
ts = Web_Socket(path, p_recv, flag, out)

ead = threading.Thread(target=ts.run, name="Guy")
ead.start()

print("Go")
from time import sleep
sleep(10)
print("Send")
p_send.send("Ho")
print("Sent")
#sleep(2)
print("Send")
p_send.send("Hoi")
print("Sent")
sleep(5)
flag.set()
p_send.send("Huh")
sleep(5)
sys.stderr.write("Do")
ead.join(10)
if ead.is_alive(): sys.stderr.write("no")
else: sys.stderr.write("ne\n")
