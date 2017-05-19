import pymongo
from pymongo import MongoClient

class dbWrapper():
	"""docstring for dbWrapper"""
	def __init__(self):
		self.cl = MongoClient() #basic connection
		self.wvs = self.cl['wvs']#here is the db name

	def getAllCheatsheets(self):
		"""
		gets all the cheatsheets and fingerprints from the db to dictionary and returns it. 
		"""
		dic = {}
		dic['sqli_fp'] = list(self.wvs.sqli_fp.find())
		dic['sqli_cs'] = list(self.wvs.sqli_cs.find())
		dic['lfi_cs'] = list(self.wvs.lfi_cs.find())
		dic['rfi_cs'] = list(self.wvs.rfi_cs.find())
		dic['ce_cs'] = list(self.wvs.ce_cs.find())
		dic['xss_cs'] = list(self.wvs.xss_cs.find())
		return dic

	def add_link_to_db(self, hash_str, link):
		"""
		gets hash string and link and insert the link to it's scan(by the hash string). 
		"""
		curr_scan = self.get_scan_by_hash(hash_str)
		self.remove_if_exist(hash_str)
		cloner = curr_scan["links"]
		cloner.append(link)
		curr_scan.update({"links" : cloner})
		self.wvs.scans.insert_one(curr_scan)

	def add_vuln_to_db(self, hash_str, vuln):
		"""
		gets hash string and vulnerable link and insert the link to it's scan(by the hash string).
		"""
		curr_scan = self.get_scan_by_hash(hash_str)
		self.remove_if_exist(hash_str)
		cloner = curr_scan["vulnLinks"]
		cloner.append(vuln)
		curr_scan.update({"vulnLinks" : cloner})
		self.wvs.scans.insert_one(curr_scan)

	def add_form_to_db(self, hash_str, form):
		"""
		gets hash string and form and insert the form to it's scan(by the hash string).
		"""
		curr_scan = self.get_scan_by_hash(hash_str)
		self.remove_if_exist(hash_str)
		cloner = curr_scan["forms"]
		cloner.append(form)
		curr_scan.update({"forms" : cloner})
		self.wvs.scans.insert_one(curr_scan)

	def done(self, hash_str):
		"""
		gets hash string and set it's project to done status.
		"""
		curr_scan = self.get_scan_by_hash(hash_str)
		self.remove_if_exist(hash_str)
		curr_scan.update({"done" : "done"})
		self.wvs.scans.insert_one(curr_scan)

	def error(self, error_msg, hash_str):
		"""
		gets hash string ans error message and insert this error to it's scan. 
		"""
		curr_scan = self.get_scan_by_hash(hash_str)
		if curr_scan["error"] == "":
			self.remove_if_exist(hash_str)
			curr_scan.update({"error" : error_msg})
			self.wvs.scans.insert_one(curr_scan)
			self.done(hash_str)

	def get_scan_by_hash(self, hash_str):
		"""
		gets hash string(ID) and returns it's scan.
		"""
		return self.wvs.scans.find_one({"hash_str" : hash_str})

	def get_all_scans(self,):
		"""
		returns all the scans.
		"""
		return self.wvs.scans.find()

	def remove_if_exist(self, hash_str):
		"""
		gets hash string and returns it's scan.
		"""
		self.wvs.scans.remove({"hash_str" : hash_str})
	
	def add_new_scan(self, scan):
		"""
		gets scan and add the scan to the db.
		"""
		self.wvs.scans.insert_one(scan)

	def get_sqli_fp(self):
		"""
		returns the sqli fingerprints.
		"""
		return self.getAllCheatsheets()['sqli_fp'][0]["errors"]

	def get_sqli_cs(self):
		"""
		returns sqli cheatsheets.
		"""
		return (self.getAllCheatsheets()['sqli_cs'][0]["cs_classic"],self.getAllCheatsheets()['sqli_cs'][1]["cs_blind"])

	def get_rfi_cs(self):
		"""
		returns rfi cheatsheets.
		"""
		return self.getAllCheatsheets()['rfi_cs'][0]["cs"]	
	
	def get_lfi_cs(self):
		"""
		returns lfi cheatsheets.
		"""
		return self.getAllCheatsheets()['lfi_cs'][0]["cs"]
	
	def get_ce_cs(self):
		"""
		returns command execution cheatsheets.
		"""
		return self.getAllCheatsheets()['ce_cs'][0]["cs"]

	def get_xss_cs(self):
		"""
		returns xss cheatsheets.
		"""
		return self.getAllCheatsheets()['xss_cs'][0]["cs"]
