def server():
    from time import sleep
    from sys import stderr
    stderr.write("Hi from server\n")
    stderr.write(str(lib) + "\n")
    while kill == False:
        sleep(1)
    stderr.write("Bye\n")
    return
