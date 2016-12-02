from Helper import *

class Sqli():
	"""docstring for ClassName"""
	#liad note: url should be like : http://abcs.com/somepage.php?id=5
	DBMS_ERRORS = {# regular expressions for DBMS fingerprints
    "MySQL": ("SQL syntax.*MySQL", "Warning.*mysql_.*", "valid MySQL result", "MySqlClient\."),
    "PostgreSQL": ("PostgreSQL.*ERROR", "Warning.*\Wpg_.*", "valid PostgreSQL result", "Npgsql\."),
    "Microsoft SQL Server": ("Driver.* SQL[\-\_\ ]*Server", "OLE DB.* SQL Server", "(\W|\A)SQL Server.*Driver", "Warning.*mssql_.*", "(\W|\A)SQL Server.*[0-9a-fA-F]{8}", "(?s)Exception.*\WSystem\.Data\.SqlClient\.", "(?s)Exception.*\WRoadhouse\.Cms\."),
    "Microsoft Access": ("Microsoft Access Driver", "JET Database Engine", "Access Database Engine"),
    "Oracle": ("\bORA-[0-9][0-9][0-9][0-9]", "Oracle error", "Oracle.*Driver", "Warning.*\Woci_.*", "Warning.*\Wora_.*"),
    "IBM DB2": ("CLI Driver.*DB2", "DB2 SQL error", "\bdb2_\w+\("),
    "SQLite": ("SQLite/JDBCDriver", "SQLite.Exception", "System.Data.SQLite.SQLiteException", "Warning.*sqlite_.*", "Warning.*SQLite3::", "\[SQLITE_ERROR\]"),
    "Sybase": ("(?i)Warning.*sybase.*", "Sybase message", "Sybase.*Server message.*"),
}
	def __init__(self,se,urls):
		self.s = se
		self.urls = urls
		self.mysql_fp = ['You have an error in your SQL syntax','check the manual that corresponds',' MySQL server version \
		for the right syntax to use near','mysql']

	def errorExist(self,html):
		"""
		gets html code of a page and checks if there are some sql errors by known strings.
		"""
		for i in self.mysql_fp:
			if i in html:
				return True
		return False

	def getAllVulnLinks(self):
		vulnLinks = []
		for i in self.urls:
			if '=' in i:
				res = self.isInjectable(i)
				if res:
					vulnLinks.append((i,res))
		return vulnLinks

	def isInjectable(self,url):
		"""
		returns true if url parameter is injectable else false
		"""
		base_html = self.s.get(url).text
		ans = self.s.get(url+'\'')
		if not notFound(ans) and self.errorExist(ans.text):#non-blind
			return "non-blind"
		ans = self.s.get(url+' and 1=1')
		if ans.text == base_html:
			ans = self.s.get(url+' and 1=2')
			if self.errorExist(ans.text) or notFound(ans):#blind
				return "blind"
		return False