# -*- coding: utf-8 -*-
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
	ret = ""
	
	for link in links:
		file_req = urllib2.urlopen(link)
		file_text = file_req.read()
		lines = file_text.split("\r\n")
		for n, l in ((n, l) for (n, l) in enumerate(lines) if (n % 3 == 0) and (len(l)> 0)):
			tup = l.strip(), link
			names.append(tup)
			if target and target == tup[0]:
				ret += tup[0] + '\n'
				ret += lines[n+1] + '\n'
				ret += lines[n+2] + '\n'
				
	if target:
		return ret
	else:
		return names


def parameter_parser(args):
	print args

	ret = None
	if len(args) >1:
		ret = args[1]
	return ret


def compare_sets(subsets):
	logging.info("Several matches with request. Comparing...")

	allEqual = True
	for n, s1 in enumerate(subsets):
		i = n +1
		while i<len(subsets):
			if not s1 == subsets[i]:
				allEqual = False
				break
			i += 1
		if not allEqual: 
			break

	if allEqual:
		logging.info("All sets got are equal. No problem")
	else:
		logging.info("Got different sets. Taking one of them")
	
	return subsets[0]


def parse_TLES (data):
	lines = data.split('\n')
	if len(lines) > 3:
		subsets =[]
		l = 0
		while l < len(lines) and len(lines[l]) > 0:
			sl = [lines[l].strip('\r'), lines[l+1].strip('\r'), lines[l+2].strip('\r')]
			subsets.append(sl)
			l += 3

		lines = compare_sets(subsets)

	for l in lines:
		print l

#FILA 1
#Field 	Columns 	Content 	Example
# 1 	01–01 	Line number 	1
# 2 	03–07 	Satellite number 	25544
# 3 	08–08 	Classification (U=Unclassified) 	U
# 4 	10–11 	International Designator (Last two digits of launch year) 	98
# 5 	12–14 	International Designator (Launch number of the year) 	067
# 6 	15–17 	International Designator (piece of the launch) 	A
# 7 	19–20 	Epoch Year (last two digits of year) 	08
# 8 	21–32 	Epoch (day of the year and fractional portion of the day) 	264.51782528
# 9 	34–43 	First Time Derivative of the Mean Motion divided by two [10] 	−.00002182
#10 	45–52 	Second Time Derivative of Mean Motion divided by six (decimal point assumed) 	00000-0
#11 	54–61 	BSTAR drag term (decimal point assumed) [10] 	-11606-4
#12 	63–63 	The number 0 (originally this should have been "Ephemeris type") 	0
#13 	65–68 	Element set number. Incremented when a new TLE is generated for this object.[10] 	292
#14 	69–69 	Checksum (modulo 10) 	7
#
#FILA 2
# 1 	01–01 	Line number 	2
# 2 	03–07 	Satellite number 	25544
# 3 	09–16 	Inclination (degrees) 	51.6416
# 4 	18–25 	Right ascension of the ascending node (degrees) 	247.4627
# 5 	27–33 	Eccentricity (decimal point assumed) 	0006703
# 6 	35–42 	Argument of perigee (degrees) 	130.5360
# 7 	44–51 	Mean Anomaly (degrees) 	325.0288
# 8 	53–63 	Mean Motion (revolutions per day) 	15.72125391
# 9 	64–68 	Revolution number at epoch (revolutions) 	56353
#10 	69–69 	Checksum (modulo 10) 	7
#

def main (args):
	sat_name = parameter_parser(args)
	if sat_name:
		logging.info("Recovering " + sat_name)
		data = get_sat_name(sat_name)
		if len(data) == 0:
			logging.warn("This satellite is not registered at " + WEB)
		else: 
			orbital_data = parse_TLES(data)

	else:
		sat_names = get_sat_name()
		for n in sat_names:
			print n[0], "-->", n[1]
		return

	



if __name__ == '__main__':
	main(sys.argv)