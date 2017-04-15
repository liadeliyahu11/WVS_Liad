from Helper import *
class FileInclusion():
	"""doc string fot the class"""
	#liad note: link should be like : http://abcs.com/somepage.php?page=
	def __init__(self, se, links, forms, csl, csr):
		self.s= se
		self.links = links
		self.rfi_cs = csr
		self.rfi_text = 'this is special text to test the rfi vulnerability!!!'
		self.lfi_cs = csl
		self.forms = forms
		self.vulns = []

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

	def checkRFI(self, link_or_form):
		"""
		check if rfi exist in the givven link or form
		"""

		for cs in self.rfi_cs:
			res = link_or_form.send_padded(self.s, cs)
			if res:
				addr, ans = res
				if self.check_RFI_in_ans(ans):
					return link_or_form.pack(' RFI')
		return False
	
	def checkLFI(self, link_or_form):
		"""
		check if rfi exist in the given link
		"""
		#link handle
		for cs in self.lfi_cs:
			res = link_or_form.send_padded(self.s, cs)
			if res:
				addr, ans = res
				if self.check_LFI_in_ans(ans):
					return link_or_form.pack(' LFI')
		return False

	def getAllVulns(self):
		"""
		takes all the links and check their vulnerability.
		(padded with all the given cheatsheets).
		"""
		for link_or_form in (self.links + self.forms):
			rfi = self.checkRFI(link_or_form)
			if rfi:
				self.vulns.append(rfi)
			lfi = self.checkLFI(link_or_form)
			if lfi:
				self.vulns.append(lfi)
		return self.vulns