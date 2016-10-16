#import browsercookie
import re
from Helper import *
import threading
import os
import sys  

s = requests.Session()
#s.cookie = browsercookie.firefox()
def scanPages(filename,url,page,depth):
	"""
	scans a page.
	gets file name url page and depth(in the recursion) and returns is succeeded.
	"""
	try:
		print depth
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
	print "scan started..."
	if url[:4] != "http":
		print 'the url is not by the protocol'
	else:
		if url[:5] == "https":
			filename = url[8:].replace('/','-')
		else:
			filename = url[7:].replace('/','-')
		if scanPages(filename,url,"",0):
			f = open(filename+".txt","w")
			for i in total:
				f.write(i+"\n")
			f.close()
			print "scan completed!"
		else:
			print "can't scan the page you gave.(couldn't find the page)."

def main():
	reload(sys)  
	sys.setdefaultencoding('utf8')
	url = raw_input("please enter url for example:\n http://some.com\nurl:")
	scanAllPages(url)
	os.system("pause")
	
if __name__ == "__main__":
	main()