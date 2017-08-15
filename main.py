

#https://www.celestrak.com/NORAD/elements/
import logging
import urllib2
from xml.etree import ElementTree
logging.basicConfig(level=logging.DEBUG)


def main ():
	logging.info("Hello world")
	response = urllib2.urlopen("http://www.celestrak.com/NORAD/elements/")
	html = response.read()
	print html
	e = ElementTree.parse(html).getroot()
	for atype in e.findall('TABLE'):
		print atype



if __name__ == '__main__':
	main()