from Helper import *
class FileInclusion():
	"""doc string fot the class"""
	#liad note: url should be like : http://abcs.com/somepage.php?page=
	def __init__(self,url,se):
		self.s = se
		self.the_addr = 'http://wvstest.weebly.com'
		self.ffi_text = 'this is special text to test the rfi vulnerability!!!'
		self.lfi_string = ['/../../../../../../../../../../etc/passwd','/../../../../../../../../../../etc/passwd%00']
	
	def checkRFI(self,url):
		"""
		check if rfi exist in the givven url
		"""
		ans = self.s.get(url+self.the_addr)
		if self.rfi_text in ans.text:
			return url

	def checkLFI(self,url):
		"""
		check if rfi exist in the given url
		more linux:

		/etc/group
		/etc/hosts
		/etc/motd
		/etc/issue
		/etc/mysql/my.cnf
		/proc/self/environ
		/proc/version
		/proc/cmdline
		(need to ask dor if require) 
		
		apache:

		/etc/apache2/apache2.conf
		/usr/local/etc/apache2/httpd.conf
		/etc/httpd/conf/httpd.conf
		"""
		for lfi in self.lfi_string:
			ans = self.s.get(url+lfi) #liad note: find the linux/unix based servers
			if not notFound(ans.text):
				return url
		return None