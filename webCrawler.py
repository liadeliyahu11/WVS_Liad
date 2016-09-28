import requests
import re
from bs4 import BeautifulSoup
import threading
import os
import sys  

MAX_DEPTH = 5
MAX_THREADS = 1000
cluesForError = ["The resource you are looking","had its name changed","or is temporarily unavailable","File or directory not found","404","not found","Not Found","Not found","was not found on this server","The requested URL","ErrorDocument to handle the request"]
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
}
threads = []
allLinks = []
total = []
s = requests.Session()


def notFound(html):
	"""
	gets html code of a page and checks if page not found.
	"""
	c = 0
	for i in cluesForError:
		if i in html:
			c += 1
	if c>3:
		return True
	return False
	
def createFormsList(html):
	"""
	gets html code and creates list of tuples with form parameters : (name,action,method) 
	"""
	parameters,final_parameters = [],[]
	parsed_html = BeautifulSoup(html,'html.parser')
	for par in parsed_html.find_all('input'):
		parameters.append((par.get('name'),str(par)))
	for form in parsed_html.find_all('form'):
		for i in parameters:
			if i[1] in str(form):
				final_parameters.append((i[0],form.get('action'),form.get('method')))
				#to fix: if its GET or POST upper its doesnt work
				#liad note: if i want to save the input line so :
				#final_parameters.append((i[0],i[1],form.get('action'),form.get('method')))
	return final_parameters

def existInFile(fileName,toFind):
	"""
	get file name and string and check if the file contains the string.  
	"""
	f = open(fileName,'r')
	for i in f.readlines():
		if i[:-1]==toFind.encode('utf-8'): # without \n from the file
			return True
	return False

def scanPage(filename,url,page,depth):
	"""
	wrapping function to scanOnePage (scans a page).
	"""
	if not scanOnePage(filename,url,page,depth):
		allLinks.remove(page)
		return False
	return True

def par_to_file(i):
	"""
	prepares parameter line to the file.
	"""
	return (str(i[0]+'\t')+str(i[1]+'\t')+str(i[2])).encode('utf-8')

def linkValid(url,i):
	"""
	returns true if url is valid
	"""
	if i==url or i==url[7:] or ((i[:7]=="http://" or i[:8]=="https://") and 
		((url not in i or url[:7]+"www."+url[7:] not in i) or (url[:-1] not in i or url[:7]+"www."+url[7:-1] not in i)
		or (url not in i or url[:8]+"www."+url[8:] not in i) or (url[:-1] not in i or url[:8]+"www."+url[8:-1] not in i))):
		return False
	return True

def linkExist(url,page):
	"""
	checks if the link exist if it does returns the html else return False.
	"""
	if page[:4] == "http":
		ans = s.get(page,headers=headers)
		html = ans.text.encode('utf-8')
		if ans.status_code == 404 and notFound(html):
			ans = s.get(url+"/"+page,headers=headers)
			html = ans.text.encode('utf-8')
			if ans.status_code == 404 and notFound(html):
				return False
			else:
				url = url+"/"+page
		else:
			url = page
	else:
		ans = s.get(url+"/"+page,headers=headers)
		html = ans.text.encode('utf-8')
		if ans.status_code == 404 and notFound(html):
			return False
		else:
				url = url+"/"+page
	return (html,url)

def scanOnePage(filename,url,page,depth):
	"""
	scans a page.
	gets file name url page and depth(in the recursion) and returns is succeeded.
	"""
	try:
		my_threads = []
		base = url
		html,url = linkExist(url,page) # if not exist exception will raise
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
