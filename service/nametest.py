from time import sleep
from ground_assistant.naming import NameDB
ndb = NameDB()
ref = ndb.refresh(3)
while ref == False:
    sleep(5)
    ref = ndb.refresh(3)
ndb.close()
