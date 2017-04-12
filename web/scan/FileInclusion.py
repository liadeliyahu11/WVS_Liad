from Helper import *
class FileInclusion():
	"""doc string fot the class"""
	#liad note: url should be like : http://abcs.com/somepage.php?page=
	def __init__(self, se, urls, forms, csl, csr):
		self.s= se
		self.urls = urls
		self.addr = csr
		self.rfi_text = 'this is special text to test the rfi vulnerability!!!'
		self.lfi_string = csl
		self.lfi_links = []
		self.rfi_links = []
		self.lfi_forms = []
		self.rfi_forms = []
		self.forms = forms

	def check_RFI_in_ans(self, ans):
		"""
		gets http response and check if the special text exist in the page.
		"""
		return self.rfi_text in ans.text

	def check_LFI_in_ans(self, ans):
		"""
		gets http response and check if the /etc/passwd exist in the page. 
		"""
		return not notFound(ans) and 'root:' in ans.text

	def checkRFI(self, url_or_form, is_form = False):
		"""
		check if rfi exist in the givven url or form
		"""

		#link handle
		if not is_form:
			for cs in self.addr:
				res = url_or_form.send_padded_link(self.s, cs)
				if res:
					urlAddr, ans = res
					if self.check_RFI_in_ans(ans):
						return str(urlAddr).replace(" ","") + ' rfi'
		#form handle
		else:
			for cs in self.addr:
				res = url_or_form.send_padded_form(self.s, cs)
				if res:
					form, ans = res
					if self.check_RFI_in_ans(ans):
						return str(form)[2:-1].replace(" ","") + ' rfi'
		return False
	
	def checkLFI(self, url_or_form, is_form=False):
		"""
		check if rfi exist in the given url
		"""
		#link handle
		if not is_form:
			for lfi in self.lfi_string:
				res = url_or_form.send_padded_link(self.s, lfi)
				if res:
					urlAddr, ans = res
					if self.check_LFI_in_ans(ans):
						return str(urlAddr).replace(" ","") + ' lfi'
		#form handle
		else:
			for lfi in self.lfi_string:
				res = url_or_form.send_padded_form(self.s, lfi)
				if res:
					form, ans = res
					if self.check_LFI_in_ans(ans):#tuple (form string, ans)
						return str(form)[2:-1].replace(" ","") + ' lfi'
		return False

	def getAllVulnLinks(self):
		"""
		takes all the links and check their vulnerability.
		(padded with all the given cheatsheets).
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
		
	def getAllVulnForms(self):
		"""
		takes all the forms and check their vulnerability.
		(padded with all the given cheatsheets).
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