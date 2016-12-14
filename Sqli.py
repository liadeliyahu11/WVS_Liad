from Helper import *

class Sqli():
	"""docstring for ClassName"""
	#liad note: url should be like : http://abcs.com/somepage.php?id=5

	def __init__(self,se,urls):
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
				res = self.isInjectable(url)
				if res:
					vulnLinks.append((url, res))
		return vulnLinks# (type,db_type)

	def isInjectable(self,url):
		"""
		returns true if url parameter is injectable else false
		"""
		try:
			base_html = self.s.get(url).text
			ans = self.s.get(url + "\'")
			db_type = self.errorExist(ans.text)
			if not notFound(ans) and db_type:#non-blind
				return ("non-blind", db_type)
			ans = self.s.get(url + " and 1=1")
			if ans.text == base_html:
				ans = self.s.get(url + " and 1=2")
				db_type = self.errorExist(ans.text)
				if notFound(ans) or db_type:#blind
					return ("blind", db_type)
			return False
		except:
			return False