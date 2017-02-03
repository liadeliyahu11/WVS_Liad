from webCrawler import *
from vulnChecker import *
from dbWrapper import *
import Helper
import sys
import json
import os
import getopt

db = dbWrapper()

def add_new_scan(hash_str, link, links, forms, vulns):
    db.remove_if_exist(hash_str)
    scan = {
        'hash_str': hash_str,
        "link": link,
        "links": links,
        "forms": forms,
        "vulnLinks": vulns,
    }
    db.add_new_scan(scan)


def getParameters(argv):
    """
    get the require parameters from the cli.
    """
    st = '\n\ntest.py -u <url> -c <cookiesFileName>\n\n'
    st += 'url for example:\nhttp://some.com\n'
    st += 'cookie file name for example:\ncookies.txt'

    cookies, url, status508, hash_str, filename = {}, None, 999, None, None

    try:
        opts, args = getopt.getopt(
            argv, "hbu:c:s:", [
                "url=", "coockies=", "hash_str="])
    except getopt.GetoptError:
        print st
        sys.exit(2)
    try:
        for opt, arg in opts:
            if opt == '-h':
                print st
                sys.exit(2)
            elif opt == '-u':
                url = arg
            elif opt == '-c':
                cookies = parseCookiesFromFile(arg)
            elif opt == '-b':
                status508 = 1
                print 'ok'
            elif opt == '-s':
                hash_str = arg

        if (url[:HTTP] != "http://") and (url[:HTTPS] != "https://"):
            print url
            print 'the url is not by the protocol'
            sys.exit(2)
        else:
            if url[:HTTPS] == "https://":
                filename = url[HTTPS:].replace('/', '-')
            else:
                filename = url[HTTP:].replace('/', '-')
    except Exception as ex:
        print ex
        sys.exit(2)
    return (url, cookies, filename, hash_str)


def main():
    reload(sys)
    sys.setdefaultencoding('utf8')
    url, cookies, filename, hash_str = getParameters(sys.argv[1:])
    print "scan started..."
    se, links, forms = scanAllPages(url, filename, cookies)
    print "scan completed!"
    if se:
        print 'vlunerabilities scan started...'
        vc = vulnChecker(se, links, forms)
        vuln_links = vc.checkAttacks()
        print "vlunerabilities scan completed..."
        add_new_scan(hash_str, url, links, forms, vuln_links)

if __name__ == "__main__":
    main()