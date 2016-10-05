from Helper import *
class FileInclusion():
	"""doc string fot the class"""
	#liad note: url should be like : http://abcs.com/somepage.php?page=
	def __init__(self,url,se):
		self.url = url
		self.s = se
		self.the_addr = 'http://wvstest.weebly.com'
		self.the_text = 'this is special text to test the rfi vulnerability!!!'
		self.lfi_string = '../../../../../../../../../../../../../../../../../../../../../../../etc/passwd'
	
	def checkRFI(self):
		"""
		check if rfi exist in the givven url
		"""
		ans = self.s.get(self.url+self.the_addr)
		if self.the_text in ans.text:
			return url

	def checkLFI(self):
		"""
		check if rfi exist in the givven url
		more:
		/etc/group
		/etc/hosts
		/etc/motd
		/etc/issue
		/etc/mysql/my.cnf
		/proc/self/environ
		/proc/version
		/proc/cmdline
		test null %00 later
		"""
		ans = self.s.get(self.url+self.lfi_string) #liad note: find the linux/unix based servers
		if not notFound(ans.text):
			return url