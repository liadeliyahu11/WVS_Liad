from Helper import *

class Sqli():
	"""docstring for ClassName"""
	#liad note: url should be like : http://abcs.com/somepage.php?id=5
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