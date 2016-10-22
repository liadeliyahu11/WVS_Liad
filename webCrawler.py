#import browsercookie
import re
from Helper import *
import threading
import os
import sys  
import getopt


s = requests.Session()
#s.cookie = browsercookie.firefox()
def scanPages(filename,url,page,depth):
	"""
	scans a page.
	gets file name url page and depth(in the recursion) and returns is succeeded.
	"""
	try:
		my_threads = []
		base = url
		html,url = linkExist(s,url,page) # if not exist exception will raise
		if not already_visited(html) and len(total)<MAX_LINKS:
			parameters = createFormsList(html)
			if depth <=MAX_DEPTH:
				links = re.findall("href=\"([^\"]*)\"",html)
				total.append(url)
				for i in links:
					if i.encode('utf-8') not in allLinks and linkValid(base,i):#doesnt exist and doesnt equal to this url
						allLinks.append(i)
						if len(threads)<=MAX_THREADS:#if not in max threads
							t = threading.Thread(target=scanPages,args=(filename,url,i,depth+1))
							threads.append(t)
							my_threads.append(t)
							t.start()
				for i in my_threads:
					i.join()
			if print_par_to_file(filename,url,parameters):
				return True
	except Exception as ex:
		pass
	return False

def scanAllPages(url):
	"""
	gets url address and trys to scan all it's pages. 
	"""
	filename = False
	print "scan started..."
	if url[:HTTPORHTTPS] != "http":
		print 'the url is not by the protocol'
	else:
		if url[:HTTPS] == "https://":
			filename = url[HTTPS:].replace('/','-')
		else:
			filename = url[HTTP:].replace('/','-')
		if scanPages(filename,url,"",0):
			f = open(filename+".txt","w")
			for i in total:
				f.write(i+"\n")
			f.close()
			print "scan completed!"
		else:
			print "can't scan the page you gave.(couldn't find the page)."
	return filename

def getParameters(argv):
	st = '\n\ntest.py -u <url> -c <cookiesFileName>\n\n'
	st += 'url for example:\nhttp://some.com\n'
	st += 'cookie file name for example:\ncookies.txt'
	cookie_file_name = None
	url = None
	try:
		opts, args = getopt.getopt(argv,"hu:c:",["url=","coockies="])
	except getopt.GetoptError:
		print st
		sys.exit(2)
	for opt,arg in opts:
		if opt == '-h':
			print st
		elif opt == '-u':
			url = arg
		elif opt == '-c':
			cookie_file_name = arg
	return (url,cookie_file_name)