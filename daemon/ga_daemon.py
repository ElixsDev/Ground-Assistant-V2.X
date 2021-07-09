#This is the daemon for the aprs_logger / ground-assistant. If you have problems with the code or questions about it, feel free to contact me via eliservices.server@gmail.com.
import sys, os, signal, time

try:
    from processnamer import processGame
    from ground_assistant.aprs import aprs_logger
    from ground_assistant.naming import NameDB
except:
    sys.stderr.write(time.ctime().split()[3] + ": ga_daemon: ImportError\n")                         #The errors will be shown in the conosle. This becomes important if the process restarts itself.
    sys.exit()

try:
    name = "ga_daemon"
    prc = processGame()                                                                              #Create the processGame object. This creates some additional varaibles.

    if prc.prcname != name:                                                                          #prc.prcname is the name of the process that you can also see by typing "ps" into your console
        prc.nameStart(name,prc.script)                                                               #Starts this script again, but with the process name "ga_daemon",
        prc.close()
        os._exit(0)                                                                                  #and exits without raising an exception.

    prc.close()                                                                                      #Cleaning the object

except:
    sys.stderr.write(time.ctime().split()[3] + ": " + prc.prcname + ": ProcessRenameError\n")
    sys.exit()


def close(signum, stack_frame):
    #if _kill == False: return
    #_kill = True
    data.out.write(time.ctime().split()[3] + ": " + prc.prcname + ": Started exit procedure...\n")
    data.close()                                                                                #Closes everything except for the log file
    data.out.write(time.ctime().split()[3] + " " + prc.prcname + ": Library stoped, successfull clean exit.\n")
    data.out.flush()
    data.out.close()                                                                                 #Close logfile

#global _kill
#_kill = False


def checkError(command="pass"):                                                                      #Every method that needs to be called at startup could return errors via self.error
    exec(command)                                                                                    #And this just saves one line of code each time called and its kinda cool
    try:
        data.out.write(data.error)
    except:
        data.out.write(data.result)

path = os.path.abspath(".")
data = aprs_logger(path)                                                                             #Create aprs_logger object
checkError()                                                                                         #Checking for errors
data.out.write(data.version() + "\n")

#data.out.write(time.ctime().split()[3] + ": " + prc.prcname + ": Refreshing NameDB...\n")
#ndb = NameDB()
#ndb.refresh()                                                                                        #Update NameDB; This can take more time than the rest of the loading together
#data.out.write(time.ctime().split()[3] + ": " + prc.prcname + ": Done.\n")
#data.out.write("\n")                                                                                 #Makes it look cleaner
#if data.config[1] == "logfile": data.out.flush()                                                     #If a real file is used, this fixes the issue that messages go issing if the program crashes somewhere

signal.signal(signal.SIGUSR1, close)

children = data.create_listeners(processGame)
if children[0].is_alive() == False:
    data.out.write(time.ctime().split()[3] + " " + prc.prcname + ": rtd process died.\n")

if children[1].is_alive() == False:
    data.out.write(time.ctime().split()[3] + " " + prc.prcname + ": dbl process died.\n")

data.client.run(callback=data.process_beacon, autoreconnect=True)
