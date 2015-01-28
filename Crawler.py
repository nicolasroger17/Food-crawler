import requests
from bs4 import BeautifulSoup
from Parser import *
import json

class Crawler:
	def __init__(self, url):
		print str("Crawler : " + url)
		self.request = requests.get(url)
		self.urlPrefix = url[:find_nth(url, "/", 3)]
		self.content = BeautifulSoup(self.request.content)
	
	def parseForLinks(self):
		dico = {}
		for a in self.content.find_all("a"):
			a = BeautifulSoup(str(a)).a
			if(a.has_attr('href') and (a['href'][:5] == "/wiki")):
				u = str(self.urlPrefix + a['href'])
				r = requests.get(u)
				p = Parser(r.content, r.url)
				d = p.cleanAndRun()
				if(d):
					dico = dict(dico.items() + d.items())

		f = open('output.json', 'w')
		f.write(json.dumps(dico))
		f.close()

def find_nth(haystack, needle, n):
	start = haystack.find(needle)
	while start >= 0 and n > 1:
		start = haystack.find(needle, start+len(needle))
		n -= 1
	return start
