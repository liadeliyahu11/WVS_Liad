from bs4 import BeautifulSoup
import requests
from Link import *
MAX_DEPTH = 5
MAX_LINKS = 20
MAX_THREADS = 1000
HTTP = 7
HTTPS = 8

cluesForError = ["The resource you are looking","had its name changed","or is temporarily unavailable","File or directory not found","404","not found","Not Found","Not found","was not found on this server","The requested URL","ErrorDocument to handle the request"]
headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
}
threads = []
allLinks = []
total = []
pages_len = []

def parseCookiesFromFile(filename):
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
		return (ans.status_code == 404)
	return False

def already_visited(html):
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
	f.close()
	for i in lines:
		if i[:-1] == toFind.encode('utf-8'): # without \n from the file
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
	prepares parameter line to the file.(name,action,method)
	"""
	st = str(i[0])+"\t"+str(i[1])+"\n"
	for j in i[2]:
		st += j+"\n"
	return st.encode('utf-8')

def print_par_to_file(filename,url,parameters):
	try:	
		filename  = filename+"-forms.txt"
		f = open(filename,'a+')
		tagOpen = False
		for l in parameters:
			st = (str(l[0])+"\t"+str(l[1]))
			if not existInFile(filename,st):
				if not tagOpen:
					f.write("url:"+"\n"+url+"\n")
					tagOpen = True
				f.write(par_to_file(l))
			if tagOpen:
				f.write("endUrl\n")
				tagOpen = False
		f.close()
		return True
	except Exception as ex:
		print ex
	

def linkValid(url,url2):
	"""
	returns true if url is valid. include http/https and link to the same 
	"""
	IS_HTTPS = (url[:HTTPS] == "https://")
	SAME = (url2==url or url2 == url[HTTP:]) 
	IS_LINK = (url2[:HTTP]=="http://" or url2[:HTTPS]=="https://") 
	INSIDE_HTTP = (url in url2 or url[:HTTP]+"www."+url[HTTP:] in url2) 
	INSIDE_HTTP_WITHOUT_LAST =  ((url[:-1] in url2) or (url[:HTTP]+"www."+url[HTTP:-1] in url2))
	INSIDE_HTTPS = ((url in url2) or (url[:HTTPS]+"www."+url[HTTPS:] in url2)) 
	INSIDE_HTTPS_WITHOUT_LAST = ((url[:-1] in url2) or (url[:HTTPS]+"www."+url[HTTPS:-1] in url2)) 
	if (not SAME) and IS_LINK :
		if IS_HTTPS:
			return (INSIDE_HTTPS or INSIDE_HTTPS_WITHOUT_LAST)
		else:
			return (INSIDE_HTTP or INSIDE_HTTP_WITHOUT_LAST)
	return False

def linkExist(s,url,page):
	"""
	checks if the link exist if it does returns the html else return False.
	"""
	if page[:HTTP] == "http://":
		ans = s.get(page,headers=headers)
		html = ans.text.encode('utf-8')
		if notFound(ans):
			ans = s.get(url+"/"+page,headers=headers)
			html = ans.text.encode('utf-8')
			if notFound(ans):
				return False
			else:
				url = url+"/"+page
		else:
			url = page
	else:
		ans = s.get(url+"/"+page,headers=headers)
		html = ans.text.encode('utf-8')
		if notFound(ans):
			return False
		else:
				url = url+"/"+page
	return (html,url)

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