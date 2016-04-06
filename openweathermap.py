# -*- coding: utf-8 -*-
# Script to read temperature from openweathermap and write to a collectionn in RethinkDB

import requests
import rethinkdb as rdb
import time, json

with open('config.json') as file:
    conf = json.load(file)

def readData():
	r = requests.get('http://api.openweathermap.org/data/2.5/weather?q=Cacere&units=metric&APPID=' + conf["APPID"])
	temp = r.json()["main"]["temp"]
	hum = r.json()["main"]["humidity"]
	#print temp, hum, rdb.now().in_timezone('+02:00')
	conn = rdb.connect(host=conf["host"], port=conf["port"], db=conf["db"], auth_key=conf["auth_key"])
	rdb.table(conf["table"]).insert({"date": rdb.now().in_timezone('+02:00'),
                                                       "sensors":[{"name": "temp", "value": str(temp)},{"name": "hum", "value": str(hum)}]}).run(conn)
	conn.close()

while True:
	readData()
	time.sleep(1000)


