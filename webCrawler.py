#import browsercookie
import re
from Helper import *
import threading

#
#
#
#
# handle subdomains example : walla
#
#
#
#
ses = requests.Session()
#s.cookie = browsercookie.firefox()
def scanPages(filename,base_url,url=None):
	"""
	scans a page.
	gets file name, url and page. 
	returns is succeeded.
	"""
	global current_scanning
	global done
	my_threads = []
	base = base_url
	if url == None:
		url = base_url
	try:
		current_scanning += 1
		html = linkExist(ses,url)
		if html: 
			if not already_visited(html):
				total.append(url)
				current_scanning -= 1
				links = re.findall("href=\"([^\"]*)\"",html)
				for i in links:
					i = i.encode('utf-8')
					link = make_link(base,i)
					if i not in allLinks and linkValid(base,i) and not similar_page(link):#doesnt exist and doesnt equal to this url
						allLinks.append(i)
						if len(threads)<=MAX_THREADS and current_scanning+len(total) < MAX_LINKS+1 :#if not in max threads
							t = threading.Thread(target=scanPages,args=(filename,base,link))
							threads.append(t)
							my_threads.append(t)
							t.start()
				for i in my_threads:
					i.join()
				parameters = createFormsList(html)
				if print_par_to_file(filename,url,parameters):
					return True
	except Exception as ex:
		print ex
		pass
	current_scanning -= 1
	return False

def scanAllPages(url,filename,cookies):
	"""
	gets url address and trys to scan all it's pages. 
	"""
	ses.cookies.update(cookies)
	if scanPages(filename,url):
		f = open(filename+".txt","w")
		for i in total:
			f.write(i+"\n")
		f.close()
		print str(len(total)) + ' links found'
		return ses
	else:
		print "can't scan the page you gave.(couldn't find the page)."
		return False