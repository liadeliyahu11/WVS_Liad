from Sqli import *
from Link import Link
def main():
	url = raw_input("url:")
	"""s = requests.session()
	sqli = Sqli(s)
	print sqli.isInjectable(url)
	"""
	l = Link(url)
	l.getAllPossibleLinks()
	l.printLink()



if __name__ == "__main__":
	main()