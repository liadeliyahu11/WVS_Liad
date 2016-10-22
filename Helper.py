from bs4 import BeautifulSoup
import requests
from Link import *
MAX_DEPTH = 5
MAX_LINKS = 20
MAX_THREADS = 1000
HTTP = 7
HTTPS = 8
HTTPORHTTPS = 4

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
		l = line[:-1].split(':')
		if len(l)>1:
			cookies.update({l[0],l[1]})
	return cookies

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
	if url2==url or url2==url[HTTP:] or ((url2[:HTTP]=="http://" or url2[:HTTPS]=="https://") and 
		((url not in url2 or url[:HTTP]+"www."+url[HTTP:] not in url2) or (url[:-1] not in i or url[:HTTP]+"www."+url[HTTP:-1] not in url2)#with or without / 
		or (url not in url2 or url[:HTTPS]+"www."+url[HTTPS:] not in url2) or (url[:-1] not in i or url[:HTTPS]+"www."+url[HTTPS:-1] not in url2))):
		return False
	return True

def linkExist(s,url,page):
	"""
	checks if the link exist if it does returns the html else return False.
	"""
	if page[:HTTP] == "http://":
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

	"""
	the end of the functions for the crawler
	the start of the functions for the vuln scanner
	"""




def key_values_post(keys,values):# form  = [url,action,method,[key,key,key]]
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
	links = []
	f = open(filename,'r')
	lines = f.readlines()
	f.close()
	for line in lines:
		links.append(line[:-1])
	return links
def sendRequest(session,base_url,form,values):#[url,action,method,[key,key,key]]
	try:
		url,action,method,keys = form[0],form[1],form[2],form[3]
		if action != ('' or '/'):
				url=base_url+'/'+action
		print url
		if method == 'post':
			data = key_values_post(keys,values)
			ans = session.post(url,data=data)
			html = ans.text.encode('utf-8')
			if ans.status_code == 404 and notFound(html):
				return False
			return html
		elif method == 'get':
			link = Link(url)
			url = link.addGetParameters(keys,values)
			print url
			ans = session.get(url)
			html = ans.text.encode('utf-8')
			if ans.status_code == 404 and notFound(html):
				return False
			return html
	except Exception as ex:
		print ex
		pass
	return False