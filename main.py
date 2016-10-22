from webCrawler import *
from vulnChecker import *
def main():
	reload(sys)
	sys.setdefaultencoding('utf8')
	url,cookie_file_name = getParameters(sys.argv[1:])
	filename = scanAllPages(url)
	if filename:
		print 'vlunerabilities scan started...'
		vc = vulnChecker(filename+".txt",filename+"-forms.txt")
	os.system("pause")

if __name__ == "__main__":
	main()