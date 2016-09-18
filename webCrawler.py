import requests
import re
from bs4 import BeautifulSoup
import threading
import os
import sys  

cluesForError = ["404","not found","Not Found","Not found","was not found on this server","The requested URL","ErrorDocument to handle the request"]
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
}
cv = threading.Lock()

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

def scanPage(filename,url,page):
	if not scanOnePage(filename,url,page):
		f = open("errors.txt","a+")
		f.write(page+"\n")
		f.close()
		return False
	return True

def linkValidator(url,i):
	if i==url or i==url[7:] or ((i[:7]=="http://" or i[:8]=="https://") and 
		((url[7:] not in i) or (url[7:-1] not in i) or (url[8:] not in i) or (url[8:-1] not in i))):
		return False
	return True


def scanOnePage(filename,url,page):
	try:
		base = url
		ans = requests.get(url+"/"+page,headers=headers)
		html = ans.text.encode('utf-8')
		if ans.status_code == 404 and notFound(html):
			ans = requests.get(page,headers=headers)
			html = ans.text.encode('utf-8')
			if ans.status_code == 404 and notFound(html):
				return False
			else:
				url = page
		else:
			url = url+"/"+page
		parameters = createFormsList(html)
		f = open(filename+".txt",'a+')
		links = re.findall("href=\"([^\"]*)\"",html)
		for i in links:
			if not existInFile(filename+".txt",i) and linkValidator(base,i):#doesnt exist and doesnt equal to the this url
				#cv.acquire()
				f.write(i.encode('utf-8')+"\n")
				#cv.release()
		f.close()
		f = open(filename+"-forms.txt",'a+')
		tagOpen = False
		for i in parameters:
			if not existInFile(filename+"-forms.txt",str(i).encode('utf-8')):
				#cv.acquire()
				if not tagOpen:
					f.write("url:"+"\n"+url+"\n")
					tagOpen = True
				f.write(str(i).encode('utf-8')+"\n")
				#cv.release()
		#cv.acquire()
		if tagOpen:
			f.write("endUrl\n")
		#cv.release()
		f.close()
		return True
	except Exception as ex:
		print ex
		return False

def scanAllPages(url):
	threads = []
	if url[:5] == "https":
		filename = url[8:].replace('/','-')
	else:
		filename = url[7:].replace('/','-')
	if scanPage(filename,url,""):
		f = open(filename+".txt",'r')
		lines = f.readlines()
		f.close()
		f = open(filename+".txt",'w')
		f.write("\n")
		f.close()
		for i in lines:
			i = i[:-1] #without \n from the file
			t = threading.Thread(target=scanPage,args=(filename,url,i))
			threads.append(t)
			t.start()
						
	else:
		print "cant scan the page you gave"

def main():
	reload(sys)  
	sys.setdefaultencoding('utf8')
	url = raw_input("please enter url:")
	scanAllPages(url)
	os.system("pause")
	
if __name__ == "__main__":
	main()
