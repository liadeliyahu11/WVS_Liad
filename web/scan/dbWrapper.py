import pymongo
from pymongo import MongoClient

class dbWrapper():
	"""docstring for dbWrapper"""
	def __init__(self):
		self.cl = MongoClient() #basic connection
		self.wvs = self.cl['wvs']#here is the db name

	def getAllCheatsheets(self):
		dic = {}
		dic['sqli_fp'] = list(self.wvs.sqli_fp.find())
		dic['sqli_cs'] = list(self.wvs.sqli_cs.find())
		dic['lfi_cs'] = list(self.wvs.lfi_cs.find())
		dic['rfi_cs'] = list(self.wvs.rfi_cs.find())
		dic['ce_cs'] = list(self.wvs.ce_cs.find())
		dic['xss_cs'] = list(self.wvs.xss_cs.find())
		return dic

	def add_link_to_db(self, hash_str, link):
		curr_scan = self.get_scan_by_hash(hash_str)
		self.remove_if_exist(hash_str)
		cloner = curr_scan["links"]
		cloner.append(link)
		curr_scan.update({"links" : cloner})
		self.wvs.scans.insert_one(curr_scan)

	def add_vuln_to_db(self, hash_str, vuln):
		curr_scan = self.get_scan_by_hash(hash_str)
		self.remove_if_exist(hash_str)
		cloner = curr_scan["vulnLinks"]
		cloner.append(vuln)
		curr_scan.update({"vulnLinks" : cloner})
		self.wvs.scans.insert_one(curr_scan)

	def add_form_to_db(self, hash_str, form):
		curr_scan = self.get_scan_by_hash(hash_str)
		self.remove_if_exist(hash_str)
		cloner = curr_scan["forms"]
		cloner.append(form)
		curr_scan.update({"forms" : cloner})
		self.wvs.scans.insert_one(curr_scan)

	def done(self, hash_str):
		curr_scan = self.get_scan_by_hash(hash_str)
		self.remove_if_exist(hash_str)
		curr_scan.update({"done" : "done"})
		self.wvs.scans.insert_one(curr_scan)

	def error(self, error_msg, hash_str):
		curr_scan = self.get_scan_by_hash(hash_str)
		if curr_scan["error"] == "":
			self.remove_if_exist(hash_str)
			curr_scan.update({"error" : error_msg})
			self.wvs.scans.insert_one(curr_scan)
			self.done(hash_str)

	def get_scan_by_hash(self, hash_str):
		return self.wvs.scans.find_one({"hash_str" : hash_str})

	def get_all_scans(self,):
		return self.wvs.scans.find()

	def remove_if_exist(self, hash_str):
		self.wvs.scans.remove({"hash_str" : hash_str})
	
	def add_new_scan(self, scan):
		self.wvs.scans.insert_one(scan)

	def get_sqli_fp(self):
		return self.getAllCheatsheets()['sqli_fp'][0]["errors"]

	def get_sqli_cs(self):
		return (self.getAllCheatsheets()['sqli_cs'][0]["cs_classic"],self.getAllCheatsheets()['sqli_cs'][1]["cs_blind"])

	def get_rfi_cs(self):
		return self.getAllCheatsheets()['rfi_cs'][0]["cs"]	
	
	def get_lfi_cs(self):
		return self.getAllCheatsheets()['lfi_cs'][0]["cs"]
	
	def get_ce_cs(self):
		return self.getAllCheatsheets()['ce_cs'][0]["cs"]

	def get_xss_cs(self):
		return self.getAllCheatsheets()['xss_cs'][0]["cs"]
