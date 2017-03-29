from Link import *

class Form():
	"""docstring for Form"""
	def __init__(self, form_list):
		# [url, action, method, [name1, name2]]
		self.form_list = form_list
		self.url = form_list[0]
		self.action = form_list[1] 
		self.is_get = (form_list[2].lower() == 'get') if form_list[2] else True
		self.keys = form_list[3]

	def send_padded_form(self, s, cs):
		try:
			while self.url[-1] == '.':
				self.url = self.url[:-1]
			if not self.action:
				self.action = ''
			elif '#' in self.action:
					self.action = ''
			if self.action != ('' or '/'):

				self.url += '/' + self.action

			if self.is_get:
				link = Link(self.url)
				link.set_params(self.keys)
				addr, ans = link.send_padded_link(s, cs)
				return (addr, ans)
			else:
				data = self.get_padded_data(cs)
				ans = s.post(self.url, data = data)
				return (str(self.form_list), ans)
		except Exception as ex:
			print ex
			return False


	def get_padded_data(self, cs):
		"""
		chain key to value (organized  in dictionary)
		"""
		data = {}
		for key in self.keys:
			data.update({key : cs})
		return data
		
	def numOfParameters(self):
		return len(self.keys)