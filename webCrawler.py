import os
import Link
from google import google
	
links_list = []
res = google.search("site:amit-flowers.com", 20)
for i in res:
	try:
		a = Link(i.link)
		if a not in links_list:
			links_list.append(a)
	except:
		pass
for i in links_list:
	print links_list.printLink()
	
os.system("pause")