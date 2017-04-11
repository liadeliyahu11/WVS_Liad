from Helper import *
from FileInclusion import * 
from Sqli import * 
from Xss import * 
from CommandInjection import *

class vulnChecker():
	"""docstring for vulnChecker"""
	def __init__(self, se, links, forms, db):
		self.se = se
		self.db = db
		self.allLinks, self.allForms = self.filter_link_and_forms(links, forms)

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
		lrfi = FileInclusion(self.se, self.allLinks, self.allForms)
		xss = Xss(self.se, self.allLinks, self.allForms, self.db.get_xss_cs())
		sqli = Sqli(self.se, self.allLinks, self.allForms)
		ci = CommandInjection(self.se, self.allLinks, self.allForms)

		lfi, rfi = lrfi.getAllVulnLinks()
		vuln_sqli = sqli.getAllVulnLinks()
		vuln_xss =  xss.getAllVulnLinks()
		vuln_CommandInjection = ci.getAllVulnLinks()

		vuln_sqli_f = sqli.getAllVulnForms()
		vuln_xss_f = xss.getAllVulnForms()
		lfi_f, rfi_f = lrfi.getAllVulnForms()
		vuln_CommandInjection_f = ci.getAllVulnForms()
		
		print(Fore.BLUE + 'xss:')
		for vuln in vuln_xss:
			print vuln

		print(Fore.BLUE + "command injection:")
		for vuln in vuln_CommandInjection:
			print vuln

		print(Fore.BLUE + 'sql injection:')
		for vuln in vuln_sqli:
			print vuln[0] + ":" + vuln[1][0] + ":" + vuln[1][1]

		print(Fore.BLUE + 'lfi:')
		for l in lfi:
			print l 
		
		print(Fore.BLUE + 'rfi:')
		for r in rfi:
			print r

		for vuln in vuln_sqli_f:
			print vuln

		for vuln in vuln_CommandInjection_f:
			print vuln

		for vuln in vuln_xss_f:
			print vuln

		for vuln in lfi_f:
			print vuln

		for vuln in rfi_f:
			print vuln
		
		return list(lfi + rfi + vuln_sqli + vuln_xss + vuln_sqli_f + lfi_f + rfi_f + vuln_xss_f + vuln_CommandInjection_f + vuln_CommandInjection)

		#admin' and (select 1 from dual where (select password from users where username = 'admin') like '___________')#