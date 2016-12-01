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

	def sync(self, status, previousStatus):
		print status + " - " + previousStatus
		if status == previousStatus:
			return status
		else:
			if status == "stopped":
				# print "in stopped ! "
				self.stop()
				previousStatus = "stopped"
			elif status == "playing":
				# print "in playing ! "
				self.play()
				previousStatus = "playing"
			elif status == "paused":
				print "in paused ! "
				self.pause()
				# previousStatus = "paused"
		return previousStatus


def func():
	user = raw_input("Enter your VLC password:\n")

	ip = raw_input("Enter the ip of the user:\n")
	passwd = raw_input("Password:\n")

	remote = VLC(ip, passwd)
	local = VLC("localhost", user)
	print local.ip
	print remote.ip

	localBefore = local.getStatus()
	remoteBefore = remote.getStatus()

	while(True):
		localInstant = local.getStatus()
		remoteInstant = remote.getStatus()

		print localBefore + "-" + localInstant
		print remoteBefore + "-" + remoteInstant

		if localInstant != localBefore:
			if localInstant == "stopped":
				remote.stop()
				remoteBefore = "stopped"
			elif localInstant == "playing":
				remote.play()
				remoteBefore = "playing"
			elif localInstant == "paused":
				remote.pause()
				remoteBefore = "paused"
			localBefore = localInstant

		elif remoteInstant != remoteBefore:
			if remoteInstant == "stopped":
				local.stop()
				localBefore = "stopped"
			elif remoteInstant == "playing":
				local.play()
				localBefore = "playing"
			elif remoteInstant == "paused":
				local.pause()
				localBefore = "paused"
			remoteBefore = remoteInstant

		time.sleep(0.5)