from webCrawler import *
from vulnChecker import *
import Helper
import sys  
import os
import getopt

def getParameters(argv):
	"""
	get the require parameters from the cli.
	"""
	st = '\n\ntest.py -u <url> -c <cookiesFileName>\n\n'
	st += 'url for example:\nhttp://some.com\n'
	st += 'cookie file name for example:\ncookies.txt'
	cookies,url,status508 = {},None,999
	try:
		opts, args = getopt.getopt(argv,"hu:c:",["url=","coockies="])
	except getopt.GetoptError:
		print st
		sys.exit(2)
	try:
		for opt,arg in opts:
			if opt == '-h':
				print st
				sys.exit(2)
			elif opt == '-u':
				url = arg
			elif opt == '-c':
				cookies = parseCookiesFromFile(arg)
		filename = False
		if (url[:HTTP] != "http://") and (url[:HTTPS] != "https://"):
			print url
			print 'the url is not by the protocol'
			sys.exit(2)
		else:
			if url[:HTTPS] == "https://":
				filename = url[HTTPS:].replace('/','-')
			else:
				filename = url[HTTP:].replace('/','-')
	except Exception as ex:
		print ex
	return (url,cookies,filename)

def main():
	reload(sys)
	sys.setdefaultencoding('utf8')
	url,cookies,filename = getParameters(sys.argv[1:])
	print "scan started..."
	se = scanAllPages(url,filename,cookies)
	print "scan completed!"
	if se:
		print 'vlunerabilities scan started...'
		vc = vulnChecker(se,filename+".txt",filename+"-forms.txt")
		vc.checkAttacks()
		print "vlunerabilities scan completed..."
	os.system("pause")

if __name__ == "__main__":
	main()