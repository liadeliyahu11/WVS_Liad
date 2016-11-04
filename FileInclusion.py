from Helper import *
class FileInclusion():
	"""doc string fot the class"""
	#liad note: url should be like : http://abcs.com/somepage.php?page=
	def __init__(self,urls,se):
		self.s = se
		self.urls = urls
		self.the_addr = 'http://wvstest.weebly.com'
		self.ffi_text = 'this is special text to test the rfi vulnerability!!!'
		self.lfi_string = ['/../../../../../../../../../../etc/passwd','/../../../../../../../../../../etc/passwd%00']
		self.lfi_links = []
		self.rfi_links = []
	
	def checkLRFI():
		"""
		takes the urls and checks each link.
		if link found ad vulnerable its added to the links list.
		"""
		for i in self.urls:
			url = Link(i)
			if url.numOfParameters()>0:
				rfi = checkRFI(url)
				if rfi:
					self.rfi_links.append(rfi)
				lfi = checkLFI(url)
				if lfi:
					self.lfi_links.append(lfi)
		return (self.lfi_links,self.rfi_links)


	def checkRFI(self,url):#url without last parameter
		"""
		check if rfi exist in the givven url
		"""
		url = url.padGetParameters(self.the_addr)
		ans = self.s.get(url)
		if self.rfi_text in ans.text:
			return url
		return False


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
			url = url.padGetParameters(lfi)
			ans = self.s.get(url) #liad note: find the linux/unix based servers
			if not notFound(ans.text):
				return url
		return False