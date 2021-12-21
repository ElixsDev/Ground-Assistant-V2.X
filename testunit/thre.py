from threading import Thread
from time import sleep

def t1(**kwargs):
    for i in range(0, 10):
        print(kwargs["variable"] + str(i))
    return True

thread1 = Thread(target=t1, kwargs={"variable": "Hello W0rld!"})

print("defined")
thread1.start()
print("started")
t1(variable = "Bye W0rld!")
print("started second")
thread1.join()
print("joined second")
