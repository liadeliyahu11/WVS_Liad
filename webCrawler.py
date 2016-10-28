#import browsercookie
import re
from Helper import *
import threading

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

def scanAllPages(url,filename):
	"""
	gets url address and trys to scan all it's pages. 
	"""
	if scanPages(filename,url,"",0):
		f = open(filename+".txt","w")
		for i in total:
			f.write(i+"\n")
		f.close()
		return True
	else:
		print "can't scan the page you gave.(couldn't find the page)."
		return False