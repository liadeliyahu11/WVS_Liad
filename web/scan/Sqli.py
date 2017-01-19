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
		"""
		returns list of all the vulnerable links in this format : [url, vulnerability type, database type]
		"""
		vulnLinks = []
		for url in self.urls:
			if '=' in url:
				res = self.linkIsInjectable(url)
				if res:
					vulnLinks.append((url, res))
		return vulnLinks

	def getAllVulnForms(self):
		"""

		"""
		vulnForms = []
		for form in self.forms:
			res = self.formIsInjectable(form)
			if res:
				vulnForms.append((form, res))
		return vulnForms

	def is_classic(self, ans, db_type):
		"""
		returns True if classic sql injection found, else false.
		"""
		return not notFound(ans) and db_type

	def check_classic_cheat_sheet(self, url_or_form, cs, isForm=False):
		"""
		
		"""
		if isForm:
			ans = Form(url_or_form).send_padded_form(self.se, cs)
		else:
			ans = Link(url_or_form).send_padded_link(self.se, cs)
		if ans:
			db = self.errorExist(ans.text)
			if db and self.is_classic(ans, db):
				return ("classic-sql-injection", db)
		return False


	def formIsInjectable(self, form):
		"""

		"""
		types = self.check_classic_cheat_sheet(form, self.cs[0], isForm=True)
		if types:
				return types
		return False

	def linkIsInjectable(self, url):
		"""
		returns true if url parameter is injectable else false
		"""
		try:
			types = self.check_classic_cheat_sheet(url, self.cs[0])
			if types:
				return types
			#blind
		except:
			pass
		return False