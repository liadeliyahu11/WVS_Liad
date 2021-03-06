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
		"""
		gets padded result and cheatsheet and returns if injectable. 
		"""
		if res:
			addr, ans = res
			return cs.encode('utf8') in ans.text.encode('utf8')
		return False
   
	def check_injection(self, link_or_form, cs):
		"""
		gets link or form and cheatsheet and returns if injectable - wrap function.
		"""
		res = link_or_form.send_padded(self.se, cs)
		return self.is_injectable(res, cs)

	def checkXss(self, url_or_form):
		"""
		gets url or form and returns if xss exist.
		"""
		for cs in self.cheatsheets:
			if self.check_injection(url_or_form, cs):
				return True
		return False

	def getAllVulns(self):
		"""
		run the scan on all the given links and forms.
		"""
		for link_or_form in (self.links + self.forms):
			if self.checkXss(link_or_form):
				self.vulns.append(link_or_form.pack(" XSS"))
		return self.vulns