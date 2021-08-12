from ground_assistant import load, log

path = "/home/elias/dev/ground-assistant/daemon"
configs = load.ReadConfig("/home/elias/dev/ground-assistant/daemon")

logging = log.Logger(config_obj = configs, path = "/home/elias/dev/ground-assistant/backend/ground_assistant")
logging.append("Test")

sql = load.mySQL()
print(sql.sendquery("SHOW TABLES;"))
sql.commit()

sql.close()
logging.close()
