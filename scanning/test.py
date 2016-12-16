from Sqli import *
import sys  
import getopt
from Xss import * 

def main():
	#url = raw_input("url:")
	"""s = requests.session()
	sqli = Sqli(s)
	print sqli.isInjectable(url)
	"""
	"""l = Link(url)
	l.getAllPossibleLinks()
	l.printLink()
	"""
	#getAllFormsFromFile('thisislegal.com-forms.txt')
	
	"""
	html = sendRequest(requests.session(),'http://www.tab4u.com/',['http://www.tab4u.com/','/phpbb/ucp.php?mode=login&ref=players&redirect=/../players','post'
		,['username','password','sid','redirect','login','autologin']],['h3354053@mvrht.com','h3354053@mvrht.com','87ab7a921562d52c5b03904f6e7eee50','../players',''.encode('utf8'),'on'])
	if '57226' in html:
		print 'works'
	else:
		print html
		"""
	"""t = getParameters(sys.argv[1:])
	print t[0] 
	print t[1]
	"""
	"""
	global lock
	global ses
	filename = "thisis"
	if pageScan(ses,url):
		while len(allLinks)>0:
			pageScanner(ses,url)
		f = open(filename+".txt","w")
		for i in total:
			f.write(i+"\n")
		f.close()
		print str(len(total)) + ' links found'
	else:
		print "cant scan the page you gave"""
	se = requests.Session()
	#sql = Sqli(se,[])
	#print sql.isInjectable("http://www.tab4u.com/profile.php?id=57846")
	xsss = Xss(se,["http://www.tab4u.com/resultsSimple?tab=songs&type=song&q=asd&content=&max_chords=0","http://www.tab4u.com/players.php?ref=my_songs"])
	print xsss.getAllVulnLinks()
if __name__ == "__main__":
	main()