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



def notFound(html):
	c = 0
	for i in cluesForError:
		if i in html:
			c += 1
	if c>3:
		return True
	return False
	
def createFormsList(html):
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
	f = open(fileName,'r')
	for i in f.readlines():
		if i[:-1]==toFind.encode('utf-8'):
			return True
	return False

def scanPage(filename,url,page,depth):
	if not scanOnePage(filename,url,page,depth):
		allLinks.remove(page)
		return False
	return True

def linkValid(url,i):
	"""
	return true if valid
	"""
	if i==url or i==url[7:] or ((i[:7]=="http://" or i[:8]=="https://") and 
		((url not in i or url[:7]+"www."+url[7:] not in i) or (url[:-1] not in i or url[:7]+"www."+url[7:-1] not in i)
		or (url not in i or url[:8]+"www."+url[8:] not in i) or (url[:-1] not in i or url[:8]+"www."+url[8:-1] not in i))):
		return False
	return True

def linkExist(url,page):
	if page[:4] == "http":
		ans = requests.get(page,headers=headers)
		html = ans.text.encode('utf-8')
		if ans.status_code == 404 and notFound(html):
			ans = requests.get(url+"/"+page,headers=headers)
			html = ans.text.encode('utf-8')
			if ans.status_code == 404 and notFound(html):
				return False
			else:
				url = url+"/"+page
		else:
			url = page
	else:
		ans = requests.get(url+"/"+page,headers=headers)
		html = ans.text.encode('utf-8')
		if ans.status_code == 404 and notFound(html):
			return False
		else:
				url = url+"/"+page
	return (html,url)

def scanOnePage(filename,url,page,depth):
	try:
		my_threads = []
		base = url
		html,url = linkExist(url,page) # if not exist exception will raise
		parameters = createFormsList(html)
		links = re.findall("href=\"([^\"]*)\"",html)
		total.append(url)
		for i in links:
			if i.encode('utf-8') not in allLinks and linkValid(base,i):#doesnt exist and doesnt equal to this url
				allLinks.append(i)
				if depth <=MAX_DEPTH:
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
			if not existInFile(filename+"-forms.txt",str(i).encode('utf-8')):
				if not tagOpen:
					f.write("url:"+"\n"+url+"\n")
					tagOpen = True
				f.write(str(i).encode('utf-8')+"\n")
		if tagOpen:
			f.write("endUrl\n")
		f.close()
		return True
	except Exception as ex:
		pass
	return False

def scanAllPages(url):
	if url[:5] == "https":
		filename = url[8:].replace('/','-')
	else:
		filename = url[7:].replace('/','-')
	if scanPage(filename,url,"",0):
		print "scan started..."
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
