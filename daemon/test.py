from time import sleep
from sys import stdout, exit
stdout.write("Ground-Assistant Daemon Test\n\n")

#Usual start
stdout.write("Starting...             ")
from ga_daemon import Daemon
d = Daemon()
#d.prepare()
#d.run()
stdout.write("Done\n")

#Test Start/Stop
stdout.write("Start/Stop Test...      ")
sleep(2)
d.stop()
sleep(2)
d.run()
stdout.write("Done\n")

#Test Restart
stdout.write("Restart Test...         ")
d.restart()
stdout.write("Done\n")

#Test refresh_ndb
stdout.write("Refresh NameDB Test...  ")
d.refresh_ndb()
d.refresh_ndb(ifnotdoneyet=True)
stdout.write("Done\n")

#Return results
results = d.status("dual")
stdout.write("\nResults:\n" + results + "\n\n")

#Shutdown
d.close()
stdout.write("Passed\n")
exit()

