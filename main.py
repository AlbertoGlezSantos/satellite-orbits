WEB = "http://www.celestrak.com/NORAD/elements/"
import logging, sys
import urllib2
import argparse
from HTMLParser import HTMLParser
import BeautifulSoup
logging.basicConfig(level=logging.DEBUG)

def get_links():
	page = urllib2.urlopen(WEB)
	html = page.read()
	
	soup = BeautifulSoup.BeautifulSoup(html)
	links = soup.findAll('a')

	gen = (link for link in links if (len(link.contents) == 1) and ".txt" in link.get('href'))
	full_link_list = []
	for link in gen:
		#logging.debug(link.contents[0] + "-->" + link.get('href'))
		full_link_list.append(WEB + link.get('href'))

	return full_link_list

def get_sat_name(target=None):
	links = get_links()
	names = []
	
	for link in links:
		file_req = urllib2.urlopen(link)
		file_text = file_req.read()
		lines = file_text.split("\n")
		for n, l in ((n, l) for (n, l) in enumerate(lines) if (n % 3 == 0) and (len(l)> 0)):
			tup = l.strip(), link
			names.append(tup)
			if target and target == tup[0]:
				print tup
				print lines[n+1]
				print lines[n+2]

	return names


def parameter_parser(args):
	print args

	ret = None
	if len(args) >1:
		ret = args[1]
	return ret
	

def main (args):
	sat_name = parameter_parser(args)
	if sat_name:
		print "Recovering ", sat_name
		data = get_sat_name(sat_name)
	else:
		sat_names = get_sat_name()
		for n in sat_names:
			print n[0], "-->", n[1]



if __name__ == '__main__':
	main(sys.argv)