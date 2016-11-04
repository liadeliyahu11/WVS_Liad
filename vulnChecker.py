from Helper import *


class vulnChecker():
	"""docstring for vulnChecker"""
	def __init__(self,se,linksFileName,formsFileName):
		self.se = se
		self.allForms = getAllFormsFromFile(formsFileName)
		self.allLinks = getAllLinksFromFile(linksFileName)

	def checkAttacks():
		lfi,rfi = FileInclusion(self.se,self.allLinks)
		if len(lfi)>0:
			print lfi
		if len(rfi)>0:
			print rfi
		return False
