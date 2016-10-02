#import browsercookie
import re
from Helper import *
import threading
import os
import sys  

s = requests.Session()
#s.cookie = browsercookie.firefox()

def scanPage(filename,url,page,depth):
	"""
	wrapping function to scanOnePage (scans a page).
	"""
	if not scanOnePage(filename,url,page,depth):
		allLinks.remove(page)
		return False
	return True

def scanOnePage(filename,url,page,depth):
	"""
	scans a page.
	gets file name url page and depth(in the recursion) and returns is succeeded.
	"""
	try:
		my_threads = []
		base = url
		html,url = linkExist(s,url,page) # if not exist exception will raise
		parameters = createFormsList(html)
		if depth <=MAX_DEPTH:
			links = re.findall("href=\"([^\"]*)\"",html)
			total.append(url)
			for i in links:
				if i.encode('utf-8') not in allLinks and linkValid(base,i):#doesnt exist and doesnt equal to this url
					allLinks.append(i)
					if len(threads)<=MAX_THREADS:
						t = threading.Thread(target=scanOnePage,args=(filename,url,i,depth+1))
						threads.append(t)
						my_threads.append(t)
						t.start()
			for i in my_threads:
				i.join()
		f = open(filename+"-forms.txt",'a+')
		tagOpen = False
		for i in parameters:
			if not existInFile(filename+"-forms.txt",par_to_file(i)):
				if not tagOpen:
					f.write("url:"+"\n"+url+"\n")
					tagOpen = True
				f.write(par_to_file(i)+"\n")
		if tagOpen:
			f.write("endUrl\n")
		f.close()
		return True
	except Exception as ex:
		pass
	return False

def scanAllPages(url):
	"""
	gets url address and trys to scan all it's page. 
	"""
	print "scan started..."
	if url[:5] == "https":
		filename = url[8:].replace('/','-')
	else:
		filename = url[7:].replace('/','-')
	if scanPage(filename,url,"",0):
		f = open(filename+".txt","w")
		for i in total:
			f.write(i+"\n")
		f.close()
		print "scan completed!"
	else:
		print "cant scan the page you gave"

def main():
	reload(sys)  
	sys.setdefaultencoding('utf8')
	url = raw_input("please enter url for example:\n http://some.com\nurl:")
	scanAllPages(url)
	os.system("pause")
	
if __name__ == "__main__":
	main()
