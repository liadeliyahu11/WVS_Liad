from Helper import *
 
class Xss():
	"""docstring for Xss"""
	#cs = cheatsheet
	def __init__(self, se, urls, forms, cs):
		self.urls = urls
		self.se = se
		self.cheatsheets = cs
		self.vulnLinks = []
		self.forms = forms
   
	def link_is_injectable(self, link, cs):
		res = link.send_padded_link(self.se, cs)
		return self.is_injectable(res, cs)
   
	def getAllVulnLinks(self):
		for url in self.urls:
			link = Link(url)
			if self.checkXss(link):
				self.vulnLinks.append(url + " - xss")
		return self.vulnLinks
	   
	
	def formIsInjectable(self, form, cs):
		res = Form(form).send_padded_form(self.se, cs)
		return self.is_injectable(res, cs)
	   
	def is_injectable(self, res, cs):
		if res:
			addr, ans = res
			return cs.encode('utf8') in ans.text.encode('utf8')
		return False
   
	def getAllVulnForms(self):
		vulnForms = []
		for form in self.forms:
			res = self.checkXss(form, is_form=True)
			if res:
				vulnForms.append((str(form) + str(res) + " - xss"))
		return vulnForms
   
	def checkXss(self, url_or_form, is_form=False):
		if not is_form:
			for cs in self.cheatsheets:
				if self.link_is_injectable(url_or_form, cs):
					return True
		else:
			for cs in self.cheatsheets:
				if self.formIsInjectable(url_or_form, cs):
					return True
		return False