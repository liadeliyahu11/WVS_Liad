THE_ADDR = 'http://wvstest.weebly.com'
THE_TEXT = 'this is special text to test the rfi vulnerability!!!'
def checkRFI(utl):
	"""
	check if rfi exist in the givven url
	"""
	ans = requests.get(url+THE_ADDR)
	html = ans.text
	if THE_TEXT in html:
		return url