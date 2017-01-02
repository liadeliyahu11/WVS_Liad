from Helper import *

class Xss():
	"""docstring for Xss"""
	#cs = cheatsheet
	def __init__(self,se,urls,forms):
		self.urls = urls
		self.se = se
		self.cheatsheets = self.readFromFile("scan/xssCheatSheet.txt")
		self.vulnLinks = []
		self.forms = forms

	def readFromFile(self,filename):
	    f = open(filename)
	    lines = f.readlines()
	    lst = map(lambda x: x[:-1], lines)
	    f.close()
	    return lst

	def getAllVulnLinks(self):
		for url in self.urls:
			link = Link(url)
			if self.vulnLink(link):
				self.vulnLinks.append(url)
		return self.vulnLinks


	def vulnLink(self,link):
		for cheatsheet in self.cheatsheets:
			if self.include_the_script(link,cheatsheet):
				return True
		return False

	def include_the_script(self,link,cs):
		url = link.padGetParameters(cs)
		if '?' in url:
			ans = self.se.get(url)
			if cs.encode('utf8') in (ans.text).encode('utf8'):
				return True
		return False