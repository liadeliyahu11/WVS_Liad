class Link:

	def __init__(self,link):
		pre = link.split("/")
		self.baseUrl = pre[0]
		self.dirs = [x for x in pre[1:-1]]
		self.param = pre[-1]
		
	def printLink():
		print "base:" + self.baseUrl
		print "dirs:" + self.dirs
		print "parameters:" + self.param
		