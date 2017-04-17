from Helper import *

class Sqli():
	"""docstring for ClassName"""
	#liad note: link should be like : http://abcs.com/somepage.php?id=5

	def __init__(self, se, links, forms, errors, cs):
		self.dbms_errors = errors
		self.s = se
		self.links = links
		self.forms = forms
		self.classic_cs = cs[0]
		self.blind_cs = cs[1]
		self.vulns = []
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

	def check_classic_cheat_sheet(self, link_or_form):
		"""
		
		"""
		for cs in self.classic_cs: 
			addr, ans = link_or_form.send_padded(self.s, cs)
			if ans:
				db = self.errorExist(ans.text)
				if self.is_classic(ans, db):
					return (" classic-sql-injection, " + db)
		return False

	def check_blind_cheat_sheet(self, link_or_form):
		"""
		//value needed in the parameter
		"""
		for cs in self.blind_cs:
			addr, ans1 = link_or_form.send_padded(self.s, cs[0])
			addr, ans2 = link_or_form.send_padded(self.s, cs[1])
			if self.is_blind(ans1, ans2):
				return (" blind-sql-injection, unknown-db")
		return False


	def is_injectable(self, link_or_form):
		"""

		"""
		try:
			types = self.check_classic_cheat_sheet(link_or_form)
			if types:
				return types

			types = self.check_blind_cheat_sheet(link_or_form)
			if types:
				return types
		except:
			pass
		return False

	def getAllVulns(self):
		"""
		returns list of all the vulnerable links in this format : [link, vulnerability type, database type]
		"""
		for link_or_form in (self.links + self.forms):
			if link_or_form.numOfParameters() > 0:
				res = self.is_injectable(link_or_form)
				if res:
					self.vulns.append(link_or_form.pack(res))
		return self.vulns