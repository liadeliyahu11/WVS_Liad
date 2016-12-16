from Helper import *
from FileInclusion import * 
from Sqli import * 

class vulnChecker():
	"""docstring for vulnChecker"""
	def __init__(self,se,linksFileName,formsFileName):
		self.se = se
		self.allForms = getAllFormsFromFile(formsFileName)
		self.allLinks = getAllLinksFromFile(linksFileName)

	def checkAttacks(self):
		lrfi = FileInclusion(self.allLinks,self.se)
		lfi,rfi = lrfi.checkLRFI()
		sqli = Sqli(self.se,self.allLinks)
		vulnSqli = sqli.getAllVulnLinks()
		for i in vulnSqli:
			print i[0] + ":" + i[1][0] + ":" + i[1][1]
		if len(lfi)>0:
			print lfi 
		if len(rfi)>0:
			print rfi
		return False