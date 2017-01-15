from Helper import *
from FileInclusion import * 
from Sqli import * 
from Xss import * 
class vulnChecker():
	"""docstring for vulnChecker"""
	def __init__(self,se,linksFileName,formsFileName):
		self.se = se
		self.allForms = getAllFormsFromFile(formsFileName)
		self.allLinks = getAllLinksFromFile(linksFileName)

	def checkAttacks(self):
		lrfi = FileInclusion(self.se, self.allLinks, self.allForms)
		xss = Xss(self.se, self.allLinks, self.allForms)
		sqli = Sqli(self.se, self.allLinks, self.allForms)
		lfi, rfi = lrfi.checkLRFI()
		vuln_sqli = sqli.getAllVulnLinks()
		vuln_xss =  xss.getAllVulnLinks()

		vuln_sqli_f = sqli.getAllVulnForms()
		
		print 'xss:'
		for vuln in vuln_xss:
			print vuln

		print 'sql injection:'
		for vuln in vuln_sqli:
			print vuln[0] + ":" + vuln[1][0] + ":" + vuln[1][1]

		for vuln in vuln_sqli_f:
			print vuln
		
		print 'lfi:'
		if len(lfi) > 0:
			print lfi 
		
		print 'rfi:'
		if len(rfi) > 0:
			print rfi
		
		return list(lfi + rfi + vuln_sqli + vuln_xss + vuln_sqli_f)

		#admin' and (select 1 from dual where (select password from users where username = 'admin') like '___________')#