import requests
import re
import os
url = raw_input("please enter url:")
ans = requests.get(url)
html = ans.text
links = re.findall("href=\"([^\"]*)\"",html)
forms = re.findall("<form[^>]*action=\"([^\"]*)\"[^>]*method=\"([^\"]*)\"",html)
forms += re.findall("<form[^>]*method=\"([^\"]*)\"[^>]*action=\"([^\"]*)\"",html)
parameters = re.findall("<input [^>]* name=\"([^\"]*)\"",html)
for i in links:
	print i
print "\n\nparameters:\n\n"
for i in parameters:
	print i
print "\n\nforms:\n\n"
for i in forms:
	print i
print len(forms)
os.system("pause")
