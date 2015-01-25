from bs4 import BeautifulSoup
from Bdd import *

class Parser:
	def __init__(self, content):
		self.content = content

	def cleaner(self):
		self.content = self.content[self.content.index('</h2>\n<ul>\n<li><a href="/wiki') + 6:]
		pEnd = []
		try:
			pEnd.append(self.content.rindex('<h2><span class="mw-headline" id="See_also">'))
		except:
			print "fail see also"
		try:
			pEnd.append(self.content.rindex('<h2><span class="mw-headline" id="References">'))
		except:
                        print "fail references"
                try:
			pEnd.append(self.content.rindex('<h2><span class="mw-headline" id="External_links">'))
		except:
                        print "fail external links"
                try:
			pEnd.append(self.content.rindex('<h2><span class="mw-headline" id="Further_reading">'))
		except:
                        print "fail further reading"
		self.content = self.content[:min(pEnd)]

	def parse(self):
		c = BeautifulSoup(self.content)
		data = []
		for a in c.find_all("a"):
                        a = BeautifulSoup(str(a)).a
                        if(a.has_attr('title') and (a['title'][:4] != "Edit")):
                                data.append(a['title'])
		o = "["
		for x in data:
			o += str('"' + x.encode('utf-8') + '", ')
		o = o[:-2] + "],"
		o.replace(" (page does not exist)", "")
		print o
