from Helper import *

class Sqli():
	"""docstring for ClassName"""
	#liad note: url should be like : http://abcs.com/somepage.php?id=5

	def __init__(self, se, urls, forms):
		self.dbms_errors = {# regular expressions for DBMS fingerprints
	    "MySQL": ("SQL syntax.*MySQL", "Warning.*mysql_.*", "valid MySQL result", "MySqlClient\."),
	    "PostgreSQL": ("PostgreSQL.*ERROR", "Warning.*\Wpg_.*", "valid PostgreSQL result", "Npgsql\."),
	    "Microsoft SQL Server": ("Driver.* SQL[\-\_\ ]*Server", "OLE DB.* SQL Server", "(\W|\A)SQL Server.*Driver", "Warning.*mssql_.*", "(\W|\A)SQL Server.*[0-9a-fA-F]{8}", "(?s)Exception.*\WSystem\.Data\.SqlClient\.", "(?s)Exception.*\WRoadhouse\.Cms\."),
	    "Microsoft Access": ("Microsoft Access Driver", "JET Database Engine", "Access Database Engine"),
	    "Oracle": ("\bORA-[0-9][0-9][0-9][0-9]", "Oracle error", "Oracle.*Driver", "Warning.*\Woci_.*", "Warning.*\Wora_.*"),
	    "IBM DB2": ("CLI Driver.*DB2", "DB2 SQL error", "\bdb2_\w+\("),
	    "SQLite": ("SQLite/JDBCDriver", "SQLite.Exception", "System.Data.SQLite.SQLiteException", "Warning.*sqlite_.*", "Warning.*SQLite3::", "\[SQLITE_ERROR\]"),
	    "Sybase": ("(?i)Warning.*sybase.*", "Sybase message", "Sybase.*Server message.*"),
	    "MariaDB": ("SQL syntax.*MariaDB",),
	    }
		self.s = se
		self.urls = urls
		self.forms = forms
		self.cs = ["\'","\"","\' and \'1\'=\'1","\' and \'1\'=\'2"," and 1=1"," and 1=2"]

	def errorExist(self,html):
		"""
		gets html code of a page and checks if there are some sql errors by known strings.
		"""
		keys = self.dbms_errors.keys()
		for key in keys:
			for toFind in self.dbms_errors[key]:
				if re.findall(toFind, html):
					return key
		return False

	def getAllVulnLinks(self):
		vulnLinks = []
		for url in self.urls:
			if '=' in url:
				res = self.linkIsInjectable(url)
				if res:
					vulnLinks.append((url, res))
		return vulnLinks# (type,db_type)

	def getAllVulnForms(self):
		vulnForms = []
		for form in self.forms:
			res = self.formIsInjectable(form)
			print res
			if res:
				vulnForms.append((form, res))
		return vulnForms

	def check_cheat_sheet(self, url_or_form, cs, ErrorCheck=False,isForm=False):
		if isForm:
			ans = sendRequest(self.s, url_or_form, [cs for i in xrange(len(url_or_form[-1]))])
		else:
			ans = self.s.get(url_or_form + cs)
		if ans and ErrorCheck:
			return (ans, self.errorExist(ans.text))
		return ans

	def is_non_blind(self, ans, db_type):
		return not notFound(ans) and db_type

	def formIsInjectable(self, form):
		res = self.check_cheat_sheet(form, self.cs[0], ErrorCheck=True, isForm=True)
		if res:
			ans, db_type = res
			if self.is_non_blind(ans, db_type):
				return ("non-blind-sql-injection", db_type)
		return False


	def linkIsInjectable(self, url):
		"""
		returns true if url parameter is injectable else false
		"""
		try:
			ans, db_type = self.check_cheat_sheet(url, self.cs[0], ErrorCheck=True)
			if self.is_non_blind(ans, db_type):#non-blind
				return ("non-blind-sql-injection", db_type)
			
			#ans = self.check_cheat_sheet(url, " and 1=1")
			
			# TODO: blind sql injection + text for \"
			
			return False
		except:
			return False