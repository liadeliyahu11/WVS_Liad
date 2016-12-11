import MySQLdb

class dbWrapper():
	"""docstring for dbWrapper"""
	def __init__(self, host, username, pwd, dbname):
		self.db = MySQLdb.connect(host, username, pwd, dbname)
		self.cursor = self.db.cursor()

	def getAllCheatsheets(self):
		self.cursor.execute("select * from cheatsheets")
		res = self.cursor.fetchall()
		results = []
		for row in res:
			results.append((row[0],row[1]))
		return results

	
