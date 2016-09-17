import requests
import re
from bs4 import BeautifulSoup
import os
parameters,forms,final_parameters = [],[],[]


def createFormsList(html):
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

def scanPage(filename,url):
	try:
		if url[-1] == "/":
			url = url[:-1]
		ans = requests.get(url)
		html = ans.text
		parameters = createFormsList(html)
		f = open(filename+".txt",'a+')
		links = re.findall("href=\"([^\"]*)\"",html)
		for i in links:
			if not existInFile(filename+".txt",i) and i!=url and i!=url[7:]:#doesnt exist and doesnt equal to the this url
				f.write(i.encode('utf-8')+"\n")
		f.close()
		f = open(filename+"-forms.txt",'a+')
		f.write("url:"+"\n"+url+"\n")
		for i in parameters:
			if not existInFile(filename+"-forms.txt",str(i).encode('utf-8')):
				f.write(str(i).encode('utf-8')+"\n")
		f.write("endUrl\n")
		f.close()
		return True
	except Exception as ex:
		print ex
		return False

def scanAllPages(url):
	scanPage(url[7:],url)
	f = open(url[7:]+".txt",'r')
	lines = f.readlines()
	f.close()
	for i in lines:
		if not scanPage(url[7:],url+"/"+i[:-1]):
			print "first:"+url+"/"+i[:-1]
			if not scanPage(url[7:],url+i[-1]):
				print "second:"+url+i[-1]
				if not scanPage(url[7:],i[-1]):
					print "third:"+url+i[-1]
					f = open("errors.txt","a+")
					f.write(i+"\n")
					f.close()

def main():
	url = raw_input("please enter url:")
	#scanPage(url,url)
	scanAllPages(url)
	os.system("pause")
	
if __name__ == "__main__":
	main()
