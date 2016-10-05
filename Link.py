class Link:

	def __init__(self,link):
		pre = link.split("/")
		self.baseUrl = pre[0]+'//'+pre[1]+pre[2]
		self.dirs = [x for x in pre[3:-1]]
		tmp = pre[-1].split('?')
		self.fileName = tmp[0]
		self.param = ''
		if len(tmp)>1:
			tmp = tmp[1].split('&')
			self.param = map(lambda par: par.split('='),tmp)
			# param is list of parameters lists [[key,value],[key,value]] 
		
	def printLink(self):
		print "base:" + self.baseUrl
		print "dirs:" + str(self.dirs)
		print "file name:" + self.fileName
		print "parameters:" + str(self.param)

	def getAllPossibleLinks(self):
		totalLink = self.baseUrl
		tmp = map(lambda x:'/'+x,self.dir)
