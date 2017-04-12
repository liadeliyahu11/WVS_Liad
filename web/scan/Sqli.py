from Helper import *

class Sqli():
	"""docstring for ClassName"""
	#liad note: url should be like : http://abcs.com/somepage.php?id=5

	def __init__(self, se, urls, forms, errors, cs):
		self.dbms_errors = errors
		self.s = se
		self.urls = urls
		self.forms = forms
		self.classic_cs = cs[0]
		self.blind_cs = cs[1]
		#id :1 is common id - blind with no value won't work

	def errorExist(self, html):
		"""
		gets html code of a page and checks if there are some sql errors by known strings.
		"""
		keys = self.dbms_errors.keys()
		for key in keys:
			for toFind in self.dbms_errors[key]:
				if re.findall(toFind, html):
					return key
		return False

	def getAllVulnLinks(self):
		"""
		returns list of all the vulnerable links in this format : [url, vulnerability type, database type]
		"""
		vulnLinks = []
		for url in self.urls:
			if '=' in url:
				res = self.linkIsInjectable(url)
				if res:
					vulnLinks.append((url.replace(" ",""), res))
		return vulnLinks

	def getAllVulnForms(self):
		"""

		"""
		vulnForms = []
		for form in self.forms:
			res = self.formIsInjectable(form)
			if res:
				vulnForms.append((str(form)[2:-1].replace(" ",""), res))
		return vulnForms

	def is_classic(self, ans, db_type):
		"""
		returns True if classic sql injection found, else false.
		"""
		return not notFound(ans) and db_type

	def is_blind(self, ans1, ans2):
		"""
		returns True if classic sql injection found, else false.
		"""
		return ans1.text != ans2.text and len(ans1.text) > len(ans2.text)

	def check_classic_cheat_sheet(self, url_or_form, isForm=False):
		"""
		
		"""
		for cs in self.classic_cs: 
			if isForm:
				form, ans = Form(url_or_form).send_padded_form(self.s, cs)
			else:
				addr, ans = Link(url_or_form).send_padded_link(self.s, cs)

			if ans:
				db = self.errorExist(ans.text)
				if self.is_classic(ans, db):
					return (" classic-sql-injection", db)
		return False

	def check_blind_cheat_sheet(self, url_or_form, isForm=False):
		"""
		//value needed in the parameter
		"""
		for cs in self.blind_cs:
			if isForm:
				form, ans1 = Form(url_or_form).send_padded_form(self.s, cs[0])
				form, ans2 = Form(url_or_form).send_padded_form(self.s, cs[1])

			else:
				addr, ans1 = Link(url_or_form).send_padded_link(self.s, cs[0])
				addr, ans2 = Link(url_or_form).send_padded_link(self.s, cs[1])
			if self.is_blind(ans1, ans2):
				return (" blind-sql-injection - unknown-db")
		return False


	def formIsInjectable(self, form):
		"""

		"""
		try:
			types = self.check_classic_cheat_sheet(form, isForm=True)
			if types:
				return types

			types = self.check_blind_cheat_sheet(form, isForm=True)
			if types:
				return types
		except:
			pass
		return False


	def linkIsInjectable(self, url):
		"""
		returns true if url parameter is injectable else false
		"""
		try:
			types = self.check_classic_cheat_sheet(url)
			if types:
				return types
			
			types = self.check_blind_cheat_sheet(url)
			if types:
				return types
		except:
			pass
		return False
 