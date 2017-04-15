from Helper import *

class CommandInjection():
	"""docstring for CommandInjection"""
	def __init__(self, se, links, forms, cs):
		self.se = se
		self.cheatsheets = cs
		self.links = links
		self.vulns = []
		self.forms = forms

	def checkRootInAns(self, ans):
		return not notFound(ans) and 'root:' in ans.text

	def checkComInjec(self, url_or_form,):
		for cs in self.cheatsheets:
			res = url_or_form.send_padded(self.se, cs)
			if res:
				addr, ans = res
				if self.checkRootInAns(ans):
					return True
		return False

	def getAllVulns(self):
		for link_or_form in (self.links + self.forms):
			if self.checkComInjec(link_or_form):
				self.vulns.append(link_or_form.pack(" Command_Injection"))
		return self.vulns