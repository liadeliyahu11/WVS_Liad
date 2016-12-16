from webCrawler import *
from vulnChecker import *
import Helper
import sys  
import json
import os
import getopt

def add_new_scan(hash_str,link,links,vulns):
	scans = []
	with open("allScans.json") as f:
		scans = json.load(f)
	for dic in scans:
		if dic['hash_str'] == hash_str:
			scans.remove(dic)
	dic = {
	'hash_str':hash_str,
	"link":link,
	"links":links,
	"vulnLinks":vulns,
	}
	scans.append(dic)
	with open('allScans.json', 'w') as f:
		json.dump(scans, f)

def getParameters(url):
	"""
	get the require parameters from the cli.
	"""
	st = '\n\ntest.py -u <url> -c <cookiesFileName>\n\n'
	st += 'url for example:\nhttp://some.com\n'
	st += 'cookie file name for example:\ncookies.txt'
	cookies = {}
	#cookies,url,status508 = {},None,999
	"""try:
		opts, args = getopt.getopt(argv,"hu:c:",["url=","coockies="])
	except getopt.GetoptError:
		print st
		sys.exit(2)"""
	try:
		"""for opt,arg in opts:
			if opt == '-h':
				print st
				sys.exit(2)
			elif opt == '-u':
				url = arg
			elif opt == '-c':
				cookies = parseCookiesFromFile(arg)"""
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

def runScan(url,hash_str):

	reload(sys)
	sys.setdefaultencoding('utf8')
	
	url,cookies,filename = getParameters(url)
	print "scan started..."
	se = scanAllPages(url,filename,cookies)
	print "scan completed!"
	if se:
		print 'vlunerabilities scan started...'
		vc = vulnChecker(se,filename+".txt",filename+"-forms.txt")
		vulns = vc.checkAttacks()
		print "vlunerabilities scan completed..."
		add_new_scan(hash_str,url,getAllLinksFromFile(filename+'.txt'),vulns)