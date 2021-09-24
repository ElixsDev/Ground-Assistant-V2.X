from time import sleep
from sys import stderr
from ga_daemon import Daemon

d = Daemon()
stderr.write(d.status("dual"))
sleep(60)

while True:
    stderr.write(d.status("dual"))
    sleep(60)
