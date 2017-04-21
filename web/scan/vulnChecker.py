from Helper import *
from FileInclusion import * 
from Sqli import * 
from Xss import * 
from CommandInjection import *

class vulnChecker():
	"""docstring for vulnChecker"""
	def __init__(self, se, links, forms, db, hash_str):
		self.se = se
		self.db = db
		self.hash_str = hash_str
		self.allLinks, self.allForms = self.filter_link_and_forms(links, forms)
		self.allLinks = map(lambda x: Link(x), self.allLinks)
		self.allForms = map(lambda x: Form(x), self.allForms)

	def filter_link_and_forms(self, links, forms):
		"""
		gets links and forms and return just the wanted links and forms.
		how? described in the need_to_filter function.
		"""
		new_links, new_forms = [],[]
		for form in forms:
			found = False
			if not need_to_filter(form[0]) and not need_to_filter(form[1]): #0 - url | 1 - action
				new_forms.append(form)
		
		for link in links:
			if not need_to_filter(link):
				new_links.append(link)
		
		return (new_links, new_forms)


	def checkAttacks(self):
		"""
		check all the vulnerabilities in the links and forms.
		types : XSS, SQLI, RFI, LFI, COMMAND INJ.
		"""
		lrfi = FileInclusion(self.se, self.allLinks, self.allForms, self.db.get_lfi_cs(), self.db.get_rfi_cs())
		xss = Xss(self.se, self.allLinks, self.allForms, self.db.get_xss_cs())
		sqli = Sqli(self.se, self.allLinks, self.allForms, self.db.get_sqli_fp(), self.db.get_sqli_cs())
		ci = CommandInjection(self.se, self.allLinks, self.allForms, self.db.get_ce_cs(),)

		vuln_lrfi = lrfi.getAllVulns()
		for vuln in vuln_lrfi:
			db.add_vuln_to_db(self.hash_str, vuln)
		
		vuln_sqli = sqli.getAllVulns()
		for vuln in vuln_sqli:
			db.add_vuln_to_db(self.hash_str, vuln)
		
		vuln_xss =  xss.getAllVulns()
		for vuln in vuln_xss:
			db.add_vuln_to_db(self.hash_str, vuln)
		
		vuln_CommandInjection = ci.getAllVulns()
		for vuln in vuln_CommandInjection:
			db.add_vuln_to_db(self.hash_str, vuln)
		
		print(Fore.BLUE + 'xss:')
		for vuln in vuln_xss:
			print vuln

		print(Fore.BLUE + "command injection:")
		for vuln in vuln_CommandInjection:
			print vuln

		print(Fore.BLUE + 'sql injection:')
		for vuln in vuln_sqli:
			print vuln

		print(Fore.BLUE + 'LFI and RFI:')
		for l in vuln_lrfi:
			print l 
		return list(vuln_lrfi + vuln_sqli + vuln_xss + vuln_CommandInjection)

		#admin' and (select 1 from dual where (select password from users where username = 'admin') like '___________')#