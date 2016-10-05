from bs4 import BeautifulSoup
import requests
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
	"""
	gets html code of a page and checks if page not found by known strings.
	"""
	c = 0
	for i in cluesForError:
		if i in html:
			c += 1
	if c>3:
		return True
	return False

def existInFile(fileName,toFind):
	"""
	get file name and string and check if the file contains the string.  
	"""
	f = open(fileName,'r')
	for i in f.readlines():
		if i[:-1]==toFind.encode('utf-8'): # without \n from the file
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
				#liad note: if i want to save the input line so :
				#final_parameters.append((i[0],i[1],form.get('action'),form.get('method')))
	return final_parameters

def par_to_file(i):
	"""
	prepares parameter line to the file.(name,action,method)
	"""
	return (str(i[0]+'\t')+str(i[1]+'\t')+str(i[2])).encode('utf-8')

def linkValid(url,url2):
	"""
	returns true if url is valid. include http/https and link to the same 
	"""
	if url2==url or url2==url[7:] or ((url2[:7]=="http://" or url2[:8]=="https://") and 
		((url not in url2 or url[:7]+"www."+url[7:] not in url2) or (url[:-1] not in i or url[:7]+"www."+url[7:-1] not in url2)
		or (url not in url2 or url[:8]+"www."+url[8:] not in url2) or (url[:-1] not in i or url[:8]+"www."+url[8:-1] not in url2))):
		return False
	return True

def linkExist(s,url,page):
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