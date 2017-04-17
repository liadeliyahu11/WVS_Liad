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
		link = make_link(base_url, page.encode('utf8'))
		if link not in allLinks and linkValid(base_url, link) and not similar_page(link) and not is_useless_page(link):
			allLinks.append(link)


def getLinkFromList():
	if len(allLinks) > 0:
		res = allLinks[0]
		allLinks.remove(res)
		return res
	return False

def pageScanner(ses,base_url):
	try:		
		link = getLinkFromList()
		if link:
			pageScan(ses, base_url, link)
	
	except Exception as e:
		print
		pass

			
def pageScan(ses, base_url, url=None):
	global total_links
	
	if url == None:
		ans = ses.get(base_url)
		base_url = Link(ans.url).get_link_without_page()
		url = base_url
	
	try:
		if len(total_links) < MAX_LINKS:
			res = linkExist(ses, url)
			
			if res:
				url, html = res 
				if not already_visited(html):
					total_links.append(url)
					print(Fore.GREEN + url + " added!")
					links = hrefs(html)
					checkAddLink(base_url, links)
					form = createFormsList(url, html)
					all_forms.append(form)
		return True
	
	except Exception as ex:
		print ex
		pass
	return False


def scanAllPages(url, filename, cookies):
	"""
	gets url address and trys to scan all it's pages. 
	"""
	global total_links
	ses.cookies.update(cookies)
	signin(ses, url)
	if authenticate_owner(url) or pageScan(ses, url):
		while len(allLinks) > 0:
			pageScanner(ses, url)
		forms = filter_forms(all_forms)
		print str(len(total_links)) + ' links found'
		return (ses, total_links, forms)
	else:
		print "can't scan the page you gave.(couldn't find the page or can't find the wvs.txt file)."
		return False


def signin(se, url):
	data1 = {}
	f = open('login.txt', 'r')
	lines = map(lambda x: x[:-1] if x[-1] == '\n' else x, f.readlines())
	f.close()
	filename, method = lines[0].split('\t')
	for line in lines[1:]:
		key, val = line.split(':')
		data1.update({key:val})
	print method
	if method.lower() == 'post':
		ans = se.post(url + filename , data = data1)
		print data1
	else:
		st = ""
		for key in data.keys():
			st += key + "=" + data[key] + '&'
		ans = se.get(url + filename + '?' + st[:-1])