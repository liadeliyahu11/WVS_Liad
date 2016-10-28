from Helper import *


class vulnChecker():
	"""docstring for vulnChecker"""
	def __init__(self,linksFileName,formsFileName):
		self.allForms = getAllFormsFromFile(formsFileName)
		self.allLinks = getAllLinksFromFile(linksFileName)

	def checkAttacks():
		print 's'