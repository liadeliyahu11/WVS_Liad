from Sqli import *

def main():
	url = raw_input("url:")
	s = requests.session()
	sqli = Sqli(s)
	print sqli.isInjectable(url)



if __name__ == "__main__":
	main()