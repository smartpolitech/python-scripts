# -*- coding: utf-8 -*-
import requests
import rethinkdb as rdb
import time, json

with open('config.json') as file:
    conf = json.load(file)

def readData():
	r = requests.get('http://api.openweathermap.org/data/2.5/weather?q=Cacere&units=metric&APPID=' + conf["APPID"])
	temp = r.json()["main"]["temp"]
	hum = r.json()["main"]["humidity"]
	print temp, hum, rdb.now().in_timezone('+02:00').to_iso8601()
	conn = rdb.connect(host=conf["host"], port=conf["port"], db=conf["db"], auth_key=conf["auth_key"])
	rdb.table(conf["table"]).insert({"date": rdb.now().in_timezone('+02:00').to_iso8601(),
                                                       "sensors":[{"name": "temp", "value": temp},{"name": "hum", "value": hum}]}).run(conn)
	conn.close()

while True:
	readData()
	time.sleep(1800)


