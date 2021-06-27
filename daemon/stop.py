from processnamer import processGame
prc = processGame()
result = prc.nameStop("ga_daemon","SIGINT")
prc.close()
print(result.split("\n")[0])
