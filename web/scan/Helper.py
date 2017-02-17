from bs4 import BeautifulSoup
import requests
import re
from Link import *
from Form import *
MAX_LINKS = 50
MAX_THREADS = 100
HTTP = 7
HTTPS = 8
status508 = 15

cluesForError = [
	"The resource you are looking",
	"had its name changed",
	"or is temporarily unavailable",
	"File or directory not found",
	"404",
	"not found",
	"Not Found",
	"Not found",
	"was not found on this server",
	"The requested URL",
	"ErrorDocument to handle the request"]


headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
	"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
	"Accept-Encoding": "gzip, deflate, sdch",
	"Accept-Language": "en-US,en;q=0.8"}
threads = []
allLinks, all_forms, total_links = [], [], []
pages_len, similar_pages, tmpForms = [], [], []


current_scanning = 0
count_not_answered = 0
done = False


def need_to_filter(txt):
	# because they can destroy things
	if not txt:
		return False
	unwanted_pages = ['logout', 'setup', 'csrf', 'captcha']
	for unwanted in unwanted_pages:
		if unwanted in txt:
			return True

def is_useless_page(link):
	IS_PDF = (len(link) > 4 and link[-4:] == ".pdf")
	IS_JPG = (len(link) > 4 and link[-4:] == ".jpg")
	return (IS_JPG or IS_PDF)


def parseCookiesFromFile(filename):
	"""
	gets file name and parse the cookies from the file.
	"""
	cookies = {}
	f = open(filename, 'r')
	lines = f.readlines()
	f.close()
	for line in lines:
		if line[-1] == '\n':
			l = line[:-1].split(':')
		else:
			l = line.split(':')
		if len(l) > 1:
			cookies.update({l[0]: l[1]})
	return cookies


def notFound(ans):
	"""
	gets html code of a page and checks if page not found by known strings.
	"""
	if ans.status_code in [404, 400]:
		return True
	c = 0
	for i in cluesForError:
		if i in ans.text:
			c += 1
	if c > 3:
		return True
	return False


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
			new_html += line + '\n'
	if len(new_html) in pages_len:
		return True
	pages_len.append(len(new_html))
	return False


def alreadyAdded(toFind):
	"""
	get file name and string and check if the file contains the string.
	"""
	for form in tmpForms:
		if toFind == form:
			return True
	tmpForms.append(toFind)


def createFormsList(url, html):
	"""
	gets html code and creates list of lists with form parameters : [url,action,method,[name1,name2]]
	"""
	parameters, final_parameters = [], []
	parsed_html = BeautifulSoup(html, 'html.parser')
	for par in parsed_html.find_all('input'):
		parameters.append((par.get('name'), str(par)))
	for form in parsed_html.find_all('form'):
		# [url, action, method, [name1, name2]]
		form_lst = [url, form.get('action'), form.get('method'), []]
		for parameter in parameters:
			if parameter[0] and parameter[1] in str(form):
				form_lst[3].append(parameter[0])
		final_parameters.append(form_lst)
	return final_parameters


def hrefs(html):
	"""
	gets html and returns list of all the href's values.
	"""
	lst = []
	soup = BeautifulSoup(html, 'html.parser')
	for a in soup.find_all('a', href=True):
		lst.append(a['href'])
	for url in re.findall('url=(.*)\"', html):
		lst.append(url)
	return lst


def filter_forms(forms):
	"""

	"""
	total_forms = []
	try:
		for form in forms:  # form :list of lists - list of forms
			for one_form in form:
				if not alreadyAdded(one_form):
					total_forms.append(one_form)
		return total_forms
	except Exception as ex:
		print ex


def linkValid(url, url2):
	"""
	returns true if url2 is valid. include http/https and link to the same
	"""
	BASE_URL = url2.split('/')[2]
	IS_PAGE = (len(url2) > 0 and (url2[0] == '/' and '.' in url2))
	IS_HTTPS = (url[:HTTPS] == "https://")
	SAME = (url2 == url or url2 == url[HTTP:])
	IS_LINK = (url2[:HTTP] == "http://" or url2[:HTTPS] == "https://")
	INSIDE_HTTP = ((BASE_URL in url) or url[
		:HTTP] + "www." + url[HTTP:] in url2)
	INSIDE_HTTP_WITHOUT_LAST = (
		(BASE_URL in url[:-1]) or (BASE_URL in url[:HTTP] + "www." + url[HTTP:-1]))
	INSIDE_HTTPS = ((BASE_URL in url) or (
		BASE_URL in url[:HTTPS] + "www." + url[HTTPS:]))
	INSIDE_HTTPS_WITHOUT_LAST = (
		(BASE_URL in url[:-1]) or (BASE_URL in url[:HTTPS] + "www." + url[HTTPS:-1]))
	IS_SUBDOMAIN = (IS_LINK and (
		(url[HTTP:] in BASE_URL) or (url[HTTPS:] in BASE_URL)))
	if (not SAME) and ((IS_LINK and ((INSIDE_HTTPS or INSIDE_HTTPS_WITHOUT_LAST) or (
			INSIDE_HTTP or INSIDE_HTTP_WITHOUT_LAST))) or (IS_PAGE and not IS_LINK)) or IS_SUBDOMAIN:
		return True
	return False


def make_link(url, page):
	"""
	gets url and page name and create the right url for the request.
	"""
	if len(page) > HTTPS and page[
			:HTTP] == "http://" or page[:HTTPS] == "https://":
		return page
	return url + '/' + page


def linkExist(s, toAsk):
	"""
	checks if the link exist if it does returns the html else return False.
	"""
	if not need_to_filter(toAsk):
		print "c: " + toAsk
		ans = s.get(toAsk, headers=headers, timeout=3)
		if notFound(ans):
			return False
		return ans.text.encode('utf-8')
	return False