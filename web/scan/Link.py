import itertools

class Link:
	def __init__(self, link):
		self.link = link
		pre = link.split("/")
		self.baseUrl = pre[0]+'//'+pre[1]+pre[2]
		self.dirs = [x for x in pre[3:-1]]
		tmp = pre[-1].split('?')
		self.fileName = tmp[0]
		self.param = []
		if len(tmp)>1:
			self.param_for_build = tmp[1].split('&')
			self.param = map(lambda par: par.split('='),self.param_for_build)#get
			# param is list of parameters lists [[key,value],[key,value]] 
		
	def set_params(self,params):
		for parameter in params:
			self.param.append([parameter, None])

	def getUrlWithoutParameters(self):
		url = self.baseUrl
		for i in self.dirs:
			url += '/'+i
		return url+'/'+self.fileName


	def numOfParameters(self):
		return len(self.param)

	def printLink(self):
		"""
		prints the current parsed link.
		"""
		print "base:" + self.baseUrl
		print "dirs:" + str(self.dirs)
		print "file name:" + self.fileName
		print "parameters:" + str(self.param)

	def getAllPossibleLinks(self):
		"""
		changes the order of the parameters to check injectability return list of urls.
		"""
		link = self.baseUrl
		tmp = map(lambda x:'/'+x,self.dirs)
		link += "".join(tmp)
		link+= self.fileName+'?'
		tmp = map(lambda x: x+'&',self.param_for_build)
		for i in tmp:
			st=""
			for j in tmp:
				if j!=i:
					st += j
				st += i[:-1]
			tmp2.append(st)
		totalLinks = map(lambda x:link+x,tmp2)
		return totalLinks

	def get_link_without_page(self):
		return '/'.join(self.link.split('/')[:-1])

	def urlWithoutLastValue(url):
		"""
		gets url and returns the url without the value of the last parameter.
		"""
		found = False
		while not found:
			if url[-1] == '=':
				found = True
			else:
				url = url[:-1]
		return url

	def addGetParameters(self,keys,values):
		self.link.split('?')[0]
		self.link += '?'
		for i in xrange(len(keys)):
			self.link += keys[i]+'='+values[i]+'&'
		return self.link[:-1]

	def padGetParameters(self, parameter):
		ret_url = self.getUrlWithoutParameters()
		ret_url += '?'
		for par in self.param:
			ret_url += par[0] + '=' + parameter + '&' 
		return ret_url[:-1]

	def send_padded_link(self, s, cs):
		to_request = self.padGetParameters(cs)
		return (to_request, s.get(to_request))
