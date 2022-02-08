from forker import TheFork
from multiprocessing import Pipe
p_recv, p_send = Pipe()
fork = TheFork("/home/elias/dev/ground-assistant/daemon", p_recv, p_send)
print(fork.plugins)
fork.load("all")
fork.close("all")
fork.restart("all")
p_send.send("Hey")
p_send.send("KILLtest2")
p_send.send("Höyyy")
fork.restart("all")
fork.end()
