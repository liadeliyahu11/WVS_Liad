import itertools

class Link:

	def __init__(self,link):
		pre = link.split("/")
		self.baseUrl = pre[0]+'//'+pre[1]+pre[2]
		self.dirs = [x for x in pre[3:-1]]
		tmp = pre[-1].split('?')
		self.fileName = tmp[0]
		self.param = ''
		if len(tmp)>1:
			self.param_for_build = tmp[1].split('&')
			self.param = map(lambda par: par.split('='),self.param_for_build)
			# param is list of parameters lists [[key,value],[key,value]] 
		
	def printLink(self):
		print "base:" + self.baseUrl
		print "dirs:" + str(self.dirs)
		print "file name:" + self.fileName
		print "parameters:" + str(self.param)

	def getAllPossibleLinks(self):
		link = self.baseUrl
		tmp = map(lambda x:'/'+x,self.dirs)
		link += "".join(tmp)
		link+= self.fileName+'?'
		tmp = map(lambda x: x+'&',self.param_for_build)
		tmp2 = []
		for i in tmp:
			st=""
			for j in tmp:
				if j!=i:
					st += j
				st += i[:-1]
			tmp2.append(st)
		totalLinks = map(lambda x:link+x,tmp2)
		return totalLinks