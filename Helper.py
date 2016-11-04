from bs4 import BeautifulSoup
import requests
from Link import *
MAX_LINKS = 150
MAX_THREADS = 500
HTTP = 7
HTTPS = 8
status508 = 999

cluesForError = ["The resource you are looking","had its name changed","or is temporarily unavailable","File or directory not found","404","not found","Not Found","Not found","was not found on this server","The requested URL","ErrorDocument to handle the request"]
headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
}
threads = []
allLinks,total = [],[]
pages_len,similar_pages = [],[]


current_scanning = 0
count_not_answered = 0
done = False



def parseCookiesFromFile(filename):
	"""
	gets file name and parse the cookies from the file.
	"""
	cookies = {}
	f = open(filename,'r')
	lines = f.readlines()
	f.close()
	for line in lines:
		if line[-1] == '\n':
			l = line[:-1].split(':')
		else:
			l = line.split(':')
		if len(l)>1:
			cookies.update({l[0]:l[1]})
	return cookies

def notFound(ans):
	"""
	gets html code of a page and checks if page not found by known strings.
	"""

	c = 0
	for i in cluesForError:
		if i in ans.text:
			c += 1
	if c>3:
		return True
	return ans.status_code == 404


def similar_page(url):
	"""
	gets the url and checks if the url without the parameters is already visited.
	"""
	base_url = url.split('?')[0]
	if base_url in similar_pages:
		return True
	similar_pages.append(base_url)
	return False

def already_visited(html):
	"""
	gets the html and checks if the page is already visited.
	"""
	html = html.split('\n')
	new_html = ''
	for line in html:
		if not (('<title>' or '</title>') in line):
			new_html += line+'\n'
	if len(new_html) in pages_len:
		return True
	pages_len.append(len(new_html))
	return False

def existInFile(filename,toFind):
	"""
	get file name and string and check if the file contains the string.  
	"""
	f = open(filename,'r')
	lines = f.readlines()
	lines = "".join(lines)
	f.close()
	if toFind.encode('utf-8') in lines: # without \n from the file
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
		l = [form.get('action'),form.get('method'),[]] #[action,method,[name1,name2]]
		for i in parameters:
			if i[1] in str(form):
				l[2].append(i[0])
		final_parameters.append(l)
	return final_parameters
	
def par_to_file(i):
	"""
	prepares parameter line to the file.
	"""
	st = str(i[0])+"\t"+str(i[1])+"\n"
	for j in i[2]:
		st += str(j)+"\n"
	return st.encode('utf-8')

def print_par_to_file(filename,url,parameters):
	"""
	gets file,url and parameters and print the parameters to the givven file.
	"""
	try:	
		filename  = filename+"-forms.txt"
		f = open(filename,'a+')
		for l in parameters:
			st = par_to_file(l)
			if not existInFile(filename,st):
				f.write("url:"+"\n"+url+"\n")
				f.write(st)
				f.write("endUrl\n")
		f.close()
		return True
	except Exception as ex:
		print ex
	

def linkValid(url,url2):
	"""
	returns true if url is valid. include http/https and link to the same 
	"""
	IS_PAGE = (len(url2)>0 and (url2[0] == '/' or '.' in url2))
	IS_HTTPS = (url[:HTTPS] == "https://")
	SAME = (url2==url or url2 == url[HTTP:]) 
	IS_LINK = (url2[:HTTP]=="http://" or url2[:HTTPS]=="https://") 
	INSIDE_HTTP = (url in url2 or url[:HTTP]+"www."+url[HTTP:] in url2) 
	INSIDE_HTTP_WITHOUT_LAST =  ((url[:-1] in url2) or (url[:HTTP]+"www."+url[HTTP:-1] in url2))
	INSIDE_HTTPS = ((url in url2) or (url[:HTTPS]+"www."+url[HTTPS:] in url2)) 
	INSIDE_HTTPS_WITHOUT_LAST = ((url[:-1] in url2) or (url[:HTTPS]+"www."+url[HTTPS:-1] in url2)) 
	if (not SAME) and ((IS_LINK and ((INSIDE_HTTPS or INSIDE_HTTPS_WITHOUT_LAST) or (INSIDE_HTTP or INSIDE_HTTP_WITHOUT_LAST)))
	 or (IS_PAGE and not IS_LINK)):
		return True
	return False

def wait():
	"""
	thread sync function - wait (keeps just number of open requests at a moment)
	"""
	global count_not_answered
	while count_not_answered > status508:
		pass
	count_not_answered += 1


def make_link(url,page):
	"""
	gets url and page name and create the right url for the request. 
	"""
	if len(page)>HTTPS:
		if page[:HTTP] == "http://" or page[:HTTPS] == "https://":
			return page
	return url+'/'+page


def linkExist(s,toAsk):
	"""
	checks if the link exist if it does returns the html else return False.
	"""
	global count_not_answered
	wait()
	ans = s.get(toAsk,headers=headers)
	if notFound(ans):
		return False
	count_not_answered -= 1
	return ans.text



	"""
	the end of the functions for the crawler
	the start of the functions for the vuln scanner
	"""




def key_values_post(keys,values):# form  = [url,action,method,[key,key,key]]
	"""
	chain key to value (organized  in dictionary)
	"""
	d = {}
	if len(keys) == len(values):
		for i in xrange(0,len(keys)):
			d.update({keys[i]:values[i]})
	else:#one value for all keys
		for i in xrange(0,len(keys)):
			d.update({keys[i]:values})
	return d

def getAllFormsFromFile(filename):
 	"""
	parse all the forms from the forms file.
 	"""
	f = open(filename,'r')
	lines = f.readlines()
	f.close()
	st = "".join(lines)
	forms = map(lambda x: x[5:],st.split('endUrl\n'))
	allForms= [] # [[url,action,method,[key,key,key]],[url,action,method,[key,key,key]]]
	for i in forms:
		a = i.split('\n')
		if len(a)>2:
			url = a[0]
			action,method = a[1].split('\t')
			keys= []
			for j in a[2:-1]:
				keys.append(j)
			allForms.append([url,action,method,keys])
	return allForms

def getAllLinksFromFile(filename):
	"""
	read all the links from the links file.
	"""
	links = []
	f = open(filename,'r')
	lines = f.readlines()
	f.close()
	for line in lines:
		links.append(line[:-1])
	return links
def sendRequest(session,base_url,form,values):#[url,action,method,[key,key,key]]
	"""
	gets action and values to send and sends the requests with the given values.
	"""
	try:
		url,action,method,keys = form[0],form[1],form[2],form[3]
		if action != ('' or '/'):
				url=base_url+'/'+action
		print url
		if method == 'post':
			data = key_values_post(keys,values)
			ans = session.post(url,data=data)
			html = ans.text.encode('utf-8')
			if notFound(ans):
				return False
			return html
		elif method == 'get':
			link = Link(url)
			url = link.addGetParameters(keys,values)
			print url
			ans = session.get(url)
			html = ans.text.encode('utf-8')
			if notFound(ans):
				return False
			return html
	except Exception as ex:
		print ex
		pass
	return False