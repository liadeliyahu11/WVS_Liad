from Helper import *

class Sqli():
	"""docstring for ClassName"""
	#liad note: url should be like : http://abcs.com/somepage.php?id=5
	DBMS_ERRORS = {                                                                     # regular expressions used for DBMS recognition based on error message response
    "MySQL": (r"SQL syntax.*MySQL", r"Warning.*mysql_.*", r"valid MySQL result", r"MySqlClient\."),
    "PostgreSQL": (r"PostgreSQL.*ERROR", r"Warning.*\Wpg_.*", r"valid PostgreSQL result", r"Npgsql\."),
    "Microsoft SQL Server": (r"Driver.* SQL[\-\_\ ]*Server", r"OLE DB.* SQL Server", r"(\W|\A)SQL Server.*Driver", r"Warning.*mssql_.*", r"(\W|\A)SQL Server.*[0-9a-fA-F]{8}", r"(?s)Exception.*\WSystem\.Data\.SqlClient\.", r"(?s)Exception.*\WRoadhouse\.Cms\."),
    "Microsoft Access": (r"Microsoft Access Driver", r"JET Database Engine", r"Access Database Engine"),
    "Oracle": (r"\bORA-[0-9][0-9][0-9][0-9]", r"Oracle error", r"Oracle.*Driver", r"Warning.*\Woci_.*", r"Warning.*\Wora_.*"),
    "IBM DB2": (r"CLI Driver.*DB2", r"DB2 SQL error", r"\bdb2_\w+\("),
    "SQLite": (r"SQLite/JDBCDriver", r"SQLite.Exception", r"System.Data.SQLite.SQLiteException", r"Warning.*sqlite_.*", r"Warning.*SQLite3::", r"\[SQLITE_ERROR\]"),
    "Sybase": (r"(?i)Warning.*sybase.*", r"Sybase message", r"Sybase.*Server message.*"),
}
	def __init__(self,se):
		self.s = se
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

	def isInjectable(self,url):
		"""
		returns true if url parameter is injectable else false
		"""
		base_html = self.s.get(url).text
		ans = self.s.get(url+'\'')
		if not notFound(ans.text) and self.errorExist(ans.text):#non-blind
			return True
		ans = self.s.get(url+' and 1=1')
		if ans.text == base_html:
			ans = self.s.get(url+' and 1=2')
			if self.errorExist(ans.text) or notFound(ans.text):#blind
				return True 
		return False