from Sqli import *
def main():
	url = raw_input("url:")
	"""s = requests.session()
	sqli = Sqli(s)
	print sqli.isInjectable(url)
	"""
	"""l = Link(url)
	l.getAllPossibleLinks()
	l.printLink()
	"""
	#getAllFormsFromFile('thisislegal.com-forms.txt')

	html = sendRequest(requests.session(),'http://www.tab4u.com/',['http://www.tab4u.com/','/phpbb/ucp.php?mode=login&ref=players&redirect=/../players','post'
		,['username','password','sid','redirect','login','autologin']],['h3354053@mvrht.com','h3354053@mvrht.com','87ab7a921562d52c5b03904f6e7eee50','../players',''.encode('utf8'),'on'])
	if '57226' in html:
		print 'works'
	else:
		print html
if __name__ == "__main__":
	main()