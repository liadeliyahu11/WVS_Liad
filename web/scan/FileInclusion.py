from Helper import *
class FileInclusion():
	"""doc string fot the class"""
	#liad note: url should be like : http://abcs.com/somepage.php?page=
	def __init__(self,se,urls,forms):
		self.s = se
		self.urls = urls
		self.the_addr = 'http://wvstest.weebly.com'
		self.rfi_text = 'this is special text to test the rfi vulnerability!!!'
		self.lfi_string = ['/../../../../../../../../../../etc/passwd','/../../../../../../../../../../etc/passwd%00']
		self.lfi_links = []
		self.rfi_links = []
		self.forms = forms


	def checkRFI(self, url, is_form=False):#url without last parameter
		"""
		check if rfi exist in the givven url
		"""
		urlAddr = url.padGetParameters(self.the_addr)
		ans = self.s.get(urlAddr)
		if self.check_RFI_in_ans(ans):
			return urlAddr
		return False

	def check_LFI_in_ans(self, ans):
		return not notFound(ans) and 'root:' in ans.text

	def check_RFI_in_ans(self, ans):
		return self.rfi_text in ans.text
	
	def checkLFI(self, url, is_form=False):
		"""
		check if rfi exist in the given url
		"""
		for lfi in self.lfi_string:
			urlAddr = url.padGetParameters(self.lfi_string[0])
			ans = self.s.get(urlAddr)
			if self.check_LFI_in_ans(ans):
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
		