import itertools

class Link:
	def __init__(self, link):
		self.known_pages = ['php', 'asp', 'aspx', 'py', 'js', 'css', 'html', 'htm', 'jsp']
		self.text = link
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

	def get_link_without_page(self):
		if self.page_in_link():
			return '/'.join(self.text.split('/')[:-1])
		return self.text

	def page_in_link(self):
		for page in self.known_pages:
			if self.text[(len(page)+1)*(-1):-1] == '/' + page:
				return True
		return False

	def numOfParameters(self):
		return len(self.param)

	def addGetParameters(self, keys, values):
		self.text.split('?')[0]
		self.text += '?'
		for i in xrange(len(keys)):
			self.text += keys[i] + '=' + values[i] + '&'
		return self.text[:-1]

	def padGetParameters(self, parameter):
		ret_url = self.getUrlWithoutParameters()
		ret_url += '?'
		for par in self.param:
			ret_url += par[0] + '=' + parameter + '&' 
		return ret_url[:-1]

	def send_padded(self, s, cs):
		to_request = self.padGetParameters(cs)
		return (to_request, s.get(to_request))

	def pack(self, attack_type):
		return self.text.replace(" ","") + attack_type

	def is_link(self):
		return True

	def is_form(self):
		return False

