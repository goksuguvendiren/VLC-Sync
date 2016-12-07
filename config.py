#!/usr/bin/python
import os.path
import json

class config:
	def __init__(self, _uname = "", _pwd = "", _ip = "localhost", _host = "fatihbakir.net", _port = "4653", _path = "config.json"):
		self.username = _uname
		self.password = _pwd
		self.ip		  = _ip
		self.host	  = _host
		self.port	  = _port
		self.path 	  = _path

	def configure(self):
		if not os.path.isfile(self.path):
			self.username = raw_input("Username: ")
			self.password = getpass('Password: ')
			self.ip = raw_input("Ip: ")

			data = {"username": self.username, "password": self.password, "ip": self.ip, "host": self.host, "port": self.port}

			with open("config.json", "w") as conf:
				json.dump(data, conf, sort_keys = True, indent = 4,)

		with open("config.json", "r") as conf:
			data = json.load(conf)

		self.username = data["username"]
		self.password = data["password"]
		self.ip		  = data["ip"]
		self.host	  = data["host"]
		self.port	  = int(data["port"])
