import urllib2, base64, json
import time

class VLC:
	ip = "IP"
	password = "PASS"
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

def getFatihsIP():
	print "hey"
	request = urllib2.Request("http://ip.fatihbakir.net/ips.txt")
	result = urllib2.urlopen(request)
	string = result.read()
	page = json.loads(string)
	ip = page['ev']
	print ip
	return ip

#fatihIP = raw_input()
#if fatihIP == "f":
#	fatihIP = "85.110.88.111"

fatihIP = getFatihsIP()
print fatihIP

fatih = VLC(fatihIP, "12345")
goksu = VLC("localhost", "mykonos")

goksuBefore = goksu.getStatus()
fatihBefore = fatih.getStatus()


while(True):
	goksuInstant = goksu.getStatus()
	fatihInstant = fatih.getStatus()

	print goksuBefore + "-" + goksuInstant
	print fatihBefore + "-" + fatihInstant

	if goksuInstant != goksuBefore:
		if goksuInstant == "stopped":
			fatih.stop()
			fatihBefore = "stopped"
		elif goksuInstant == "playing":
			"""if (absolute(goksu.getTime - fatih.getTime) > 1):
				if fatih.getTime > goksu.getTime:
					fatih.getTime = goksu.getTime
				else if goksu.getTime > fatih.getTime:
					goksu.getTime = fatih.getTime"""
			fatih.play()
			fatihBefore = "playing"
		elif goksuInstant == "paused":
			fatih.pause()
			fatihBefore = "paused"
		goksuBefore = goksuInstant

	elif fatihInstant != fatihBefore:
		if fatihInstant == "stopped":
			goksu.stop()
			goksuBefore = "stopped"
		elif fatihInstant == "playing":
			"""if (absolute(goksu.getTime - fatih.getTime) > 1):
				if fatih.getTime > goksu.getTime:
					fatih.getTime = goksu.getTime
				else if goksu.getTime > fatih.getTime:
					goksu.getTime = fatih.getTime"""
			goksu.play()
			goksuBefore = "playing"
		elif fatihInstant == "paused":
			goksu.pause()
			goksuBefore = "paused"
		fatihBefore = fatihInstant

	time.sleep(0.5)

"""def absolute(number):
	if number > 0 :
		return number
	else if number < 0 :
		return number * (-1)
	else return 0
"""