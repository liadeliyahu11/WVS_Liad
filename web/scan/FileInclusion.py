from Helper import *
class FileInclusion():
	"""doc string fot the class"""
	#liad note: url should be like : http://abcs.com/somepage.php?page=
	def __init__(self,se,urls,forms):
		self.s= se
		self.urls = urls
		self.the_addr = 'http://wvstest.weebly.com'
		self.rfi_text = 'this is special text to test the rfi vulnerability!!!'
		self.lfi_string = ['/../../../../../../../../../../etc/passwd','/../../../../../../../../../../etc/passwd%00']
		self.lfi_links = []
		self.rfi_links = []
		self.lfi_forms = []
		self.rfi_forms = []
		self.forms = forms


	def checkRFI(self, url_or_form, is_form=False):
		"""
		check if rfi exist in the givven url or form
		"""
		if not is_form:
			urlAddr, ans = url_or_form.send_padded_link(self.s, self.the_addr)
			if self.check_RFI_in_ans(ans):
				return urlAddr
		else:
			form, ans = url_or_form.send_padded_form(self.s, self.the_addr)
			if self.check_RFI_in_ans(ans):
				return form
		return False

	def check_LFI_in_ans(self, ans):
		return not notFound(ans) and 'root:' in ans.text

	def check_RFI_in_ans(self, ans):
		return self.rfi_text in ans.text
	
	def checkLFI(self, url_or_form, is_form=False):
		"""
		check if rfi exist in the given url
		"""
		if not is_form:
			for lfi in self.lfi_string:
				urlAddr, ans = url_or_form.send_padded_link(self.s, lfi)
				if self.check_LFI_in_ans(ans):
					return urlAddr
		else:
			for lfi in self.lfi_string:
				form, ans = url_or_form.send_padded_form(self.s, lfi)
				return form
		return False

	def checkLRFI_in_links(self):
		"""
		takes the urls and checks each link.
		if link found ad vulnerable its added to the links list.
		"""
		for url in self.urls:
			link = Link(url)
			if link.numOfParameters() > 0:
				rfi = self.checkRFI(link)
				print "check vuln in:" + url
				if rfi:
					self.rfi_links.append(rfi)
				lfi = self.checkLFI(link)
				if lfi:
					self.lfi_links.append(lfi)
		return (self.lfi_links, self.rfi_links)
		
	def check_LRFI_in_forms(self):
		"""

		"""
		for form in self.forms:
			new_form = Form(form)
			if new_form.numOfParameters() > 0:
				rfi = self.checkRFI(new_form, is_form=True)
				if rfi:
					self.rfi_forms.append(rfi)
				lfi = self.checkLFI(new_form, is_form=True)
				if lfi:
					self.lfi_forms.append(lfi)
		return (self.lfi_forms, self.rfi_forms)