#This is the daemon for the aprs_logger / ground-assistant. If you have problems with the code or questions about it, feel free to contact me via eliservices.server@gmail.com.
import sys, os, time

try:
    from processnamer import processGame
    from ground_assistant.aprs import aprs_logger
except:
    sys.stderr.write(time.ctime().split()[3] + ": ga_daemon: ImportError\n")                         #The errors will be shown in the conosle. This becomes important if the process restarts itself.
    sys.exit()

try:
    name = "ga_daemon"
    prc = processGame()                                                                              #Create the processGame object. This creates some additional varaibles.

    if prc.prcname != name:                                                                          #prc.prcname is the name of the process that you can also see by typing "ps" into your console
        prc.nameStart(name,prc.script)                                                               #Starts this script again, but with the process name "ga_daemon",
        os._exit(0)                                                                                  #and exits.

except:
    sys.stderr.write(time.ctime().split()[3] + ": " + prc.prcname + ": ProcessRenameError\n")
    sys.exit()


def checkError(command="pass"):                                                                      #Every method that needs to be called at startup could return errors via self.error
    exec(command)                                                                                    #And this just saves one line of code each time called and its kinda cool
    try:
        data.out.write(data.error)
    except:
        data.out.write(data.result)

prc.close()                                                                                          #Cleaning the object

path = os.path.abspath(".")
data = aprs_logger(path)                                                                             #Create aprs_logger object
checkError()                                                                                         #Checking for errors
checkError("data.preparesql()")                                                                      #We can use the easy way here
checkError("data.version()")
data.out.write("\n")                                                                                 #Makes it look cleaner
if data.config[1] == "logfile": data.out.flush()                                                     #If a real file is used, this fixes the issue that messages go issing if the program crashes somewhere

try:
    data.client.run(callback=data.process_beacon, autoreconnect=True)                                #Kicks off the main process, can only be killed by exception

except KeyboardInterrupt:
    sys.stderr.write(time.ctime().split()[3] + ": " + prc.prcname + ": Exception\n")
    data.out.write(time.ctime().split()[3] + ": " + prc.prcname + ": Library stoped, clean exit.\n")
    #data.clean()                                                                                     #Clean and close aprs_logger
