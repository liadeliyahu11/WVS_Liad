#import browsercookie
import re
from Helper import *
import threading
ses = requests.Session()
#s.cookie = browsercookie.firefox()
lock = threading.Lock()
cond = threading.Condition()

done = False
mythreads = []

def checkAddLink(base_url,links):
	for page in links:
		link = make_link(base_url,page.encode('utf8'))
		if link not in allLinks and linkValid(base_url, link) and not similar_page(link) and not is_useless_page(link):
			allLinks.append(link)


def getLinkFromList():
	if len(allLinks)>0:
		res = allLinks[0]
		allLinks.remove(res)
		return res
	return False

def pageScanner(ses,base_url):
	try:		
		link = getLinkFromList()
		if link:
			pageScan(ses,base_url,link)
	except Exception as e:
		print
		pass

			
def pageScan(ses,base_url,url=None):
	global total
	if url == None:
		url = base_url
	try:
		if len(total) < MAX_LINKS:
			html = linkExist(ses, url)
			if html and not already_visited(html):
				total.append(url)
				print url+" added!"
				links = hrefs(html)
				checkAddLink(base_url, links)
				form = createFormsList(url, html)
				allParameters.append(form)
		return True
	except Exception as ex:
		print ex
		pass
	return False

def linksToFile(filename):
	global total
	f = open(FOLDER + filename + ".txt", "w")
	for i in total:
		f.write(i+"\n")
	f.close()


def scanAllPages(url,filename,cookies):
	"""
	gets url address and trys to scan all it's pages. 
	"""
	ses.cookies.update(cookies)
	
	#signin(ses, url)# this is for dvwa
	if pageScan(ses, url):
		while len(allLinks)>0:
			pageScanner(ses, url)
		linksToFile(filename)
		print_par_to_file(filename, allParameters)
		print str(len(total)) + ' links found'
		return ses
	else:
		print "can't scan the page you gave.(couldn't find the page)."
		return False


def signin(se,url):
		se.post(url + '/login.php',data={'username':"admin","password":"admin","Login":"Login"})