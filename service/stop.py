from processnamer import processGame
prc = processGame()
result = prc.nameStop("ga_daemon")
prc.close()
print(result)
print("done")
