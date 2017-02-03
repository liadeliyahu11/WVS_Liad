from Helper import *
from FileInclusion import * 
from Sqli import * 
from Xss import * 
class vulnChecker():
	"""docstring for vulnChecker"""
	def __init__(self, se, links, forms):
		self.se = se
		self.allLinks, self.allForms = self.filter_link_and_forms(links, forms)

	def filter_link_and_forms(self, links, forms):
		new_links, new_forms = [],[]
		for form in forms:
			found = False
			if not need_to_filter(form[0]) and not need_to_filter(form[1]):
				new_forms.append(form)
		
		for link in links:
			if not need_to_filter(link):
				new_links.append(link)
		
		return (new_links, new_forms)


	def checkAttacks(self):
		lrfi = FileInclusion(self.se, self.allLinks, self.allForms)
		xss = Xss(self.se, self.allLinks, self.allForms)
		sqli = Sqli(self.se, self.allLinks, self.allForms)

		lfi, rfi = lrfi.getAllVulnLinks()
		vuln_sqli = sqli.getAllVulnLinks()
		vuln_xss =  xss.getAllVulnLinks()

		vuln_sqli_f = sqli.getAllVulnForms()
		vuln_xss_f = xss.getAllVulnForms()
		lfi_f, rfi_f = lrfi.getAllVulnForms()
		
		print 'xss:'
		for vuln in vuln_xss:
			print vuln

		print 'sql injection:'
		for vuln in vuln_sqli:
			print vuln[0] + ":" + vuln[1][0] + ":" + vuln[1][1]

		print 'lfi:'
		for l in lfi:
			print l 
		
		print 'rfi:'
		for r in rfi:
			print r

		for vuln in vuln_sqli_f:
			print vuln

		for vuln in vuln_xss_f:
			print vuln

		for vuln in lfi_f:
			print vuln

		for vuln in rfi_f:
			print vuln
		
		return list(lfi + rfi + vuln_sqli + vuln_xss + vuln_sqli_f + lfi_f + rfi_f + vuln_xss_f)

		#admin' and (select 1 from dual where (select password from users where username = 'admin') like '___________')#