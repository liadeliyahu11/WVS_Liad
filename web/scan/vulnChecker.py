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

		lrfi = FileInclusion(self.se,self.allLinks,self.allForms)
		lfi,rfi = lrfi.checkLRFI()
		sqli = Sqli(self.se,self.allLinks,self.allForms)
		vuln_sqli = sqli.getAllVulnLinks()
		xss = Xss(self.se,self.allLinks,self.allForms)
		vuln_xss =  xss.getAllVulnLinks()
		
		print 'xss:'
		for vuln in vuln_xss:
			print vuln

		print 'sql injection:'
		for vuln in vuln_sqli:
			print vuln[0] + ":" + vuln[1][0] + ":" + vuln[1][1]
		
		print 'lfi:'
		if len(lfi) > 0:
			print lfi 
		
		print 'rfi:'
		if len(rfi) > 0:
			print rfi
		
		return list(lfi + rfi + vuln_sqli + vuln_xss)