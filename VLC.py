#!/usr/bin/python
import urllib2, base64, json
import time

class VLC:
	def __init__(self, newip, newpassword):
		self.ip = newip
		self.password = newpassword
		
	def getStatus(self):
		newRequest = urllib2.Request("http://" + self.ip + ":8080/requests/status.json")
		newbase64string = base64.encodestring('%s:%s' % ('',self.password)).replace('\n', '')
		newRequest.add_header("Authorization", "Basic %s" % newbase64string)
		newResult = urllib2.urlopen(newRequest)
		newstring = newResult.read()
		newPage = json.loads(newstring)
		status = newPage['state']
		return status

	def move(self, cmd):
		req = urllib2.Request("http://" + self.ip + ":8080/requests/status.json?command=pl_" + cmd)
		base64string = base64.encodestring('%s:%s' % ('',self.password)).replace('\n', '')
		req.add_header("Authorization", "Basic %s" % base64string)
		result = urllib2.urlopen(req)

	def play(self):	
		self.move("play")

	def stop(self):
		self.move("stop")

	def pause(self):
		self.move("pause")

	def getTime(self):
		newRequest = urllib2.Request("http://" + self.ip + ":8080/requests/status.json")
		newbase64string = base64.encodestring('%s:%s' % ('',self.password)).replace('\n', '')
		newRequest.add_header("Authorization", "Basic %s" % newbase64string)
		newResult = urllib2.urlopen(newRequest)
		newstring = newResult.read()
		newPage = json.loads(newstring)
		time = newPage['time']
		return time

	def sync(self, status, previousStatus, isSim = False):
		if status == previousStatus:
			return status
		else:
			if status == "stopped":
				if (not isSim):
					print "Changing : stop"
					self.stop()
				previousStatus = "stopped"
			elif status == "playing":
				if (not isSim):
					print "Changing : play"
					self.play()
				previousStatus = "playing"
			elif status == "paused":
				if (not isSim):
					print "Changing : pause"
					self.pause()
				previousStatus = "paused"
		return previousStatus
