
class Form():
	"""docstring for Form"""
	def __init__(self, form_list):
		self.form_list = form_list
		self.url = form[0]
		self.action = form[1]
		self.is_get = (form[2].lower() == 'get')
		self.keys = form[3]

	def send_padded_form(self, s, cs):
		try:
			if '#' in self.action:
					self.action = ''
			if self.action != ('' or '/'):
				self.url += '/' + self.action

			if self.is_get:
				link = Link(self.url)
				ans = link.send_padded_link(s, cs)
				return ans
			else:
				data = self.get_padded_data(cs)
				ans = s.post(self.url, data = data)
				return ans
		except:
			return False


	def get_padded_data(self, cs):
		"""
		chain key to value (organized  in dictionary)
		"""
		data = {}
		for key in self.keys:
			d.update({key : cs})
		return data
		
	def numOfParameters(self):
		return len(self.keys)