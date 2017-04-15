from Helper import *
 
class Xss():
	"""docstring for Xss"""
	#cs = cheatsheet
	def __init__(self, se, links, forms, cs):
		self.links = links
		self.se = se
		self.cheatsheets = cs
		self.vulns = []
		self.forms = forms
	
	def is_injectable(self, res, cs):
		if res:
			addr, ans = res
			return cs.encode('utf8') in ans.text.encode('utf8')
		return False
   
	def check_injection(self, link_or_form, cs):
		res = link_or_form.send_padded(self.se, cs)
		return self.is_injectable(res, cs)

	def checkXss(self, url_or_form):
		for cs in self.cheatsheets:
			if self.check_injection(url_or_form, cs):
				return True
		return False

	def getAllVulns(self):
		for link_or_form in (self.links + self.forms):
			if self.checkXss(link_or_form):
				self.vulns.append(link_or_form.pack(" XSS"))
		return self.vulns