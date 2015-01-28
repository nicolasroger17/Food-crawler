from bs4 import BeautifulSoup
import re

class Parser:
	def __init__(self, content, url):
		self.content = content
		self.url = url
	
	def cleanAndRun(self):
		if(self.cleaner()):
			return self.parse()

	def cleaner(self):
		try:
			self.content = self.content[self.content.index('<ul>\n<li><a href="/wiki') + 6:]
		except:
			return False
		pEnd = []
		try:
			pEnd.append(self.content.rindex('<h2><span class="mw-headline" id="See_also">'))
		except:
			pass ##print "fail see also"
		try:
			pEnd.append(self.content.rindex('<h2><span class="mw-headline" id="References">'))
		except:
                        pass ##print "fail references"
                try:
			pEnd.append(self.content.rindex('<h2><span class="mw-headline" id="External_links">'))
		except:
                        pass ##print "fail external links"
                try:
			pEnd.append(self.content.rindex('<h2><span class="mw-headline" id="Further_reading">'))
		except:
                        pass ##print "fail further reading"

		self.content = self.content.replace(" (page does not exist)", "").replace("list of ", "").replace("List of ", "").replace("lists of ", "").replace("Lists of ", "")
		try:
			self.content = self.content[:min(pEnd)]
		except:
			return False
		return True

	def parse(self):
		c = BeautifulSoup(self.content)
		data = []
		for a in c.find_all("a"):
                        a = BeautifulSoup(str(a)).a
                        if(a.has_attr('title') and (a['title'][:4] != "Edit")):
                                data.append(a['title'])

		data = list(set(data))

		uclean = self.urlLastPart()
		m = {}
		tab = []
		if(uclean.find("Wiki") == -1):
			for x in data:
				if x.find(":") == -1:
					tab.append(re.sub(r' \([^)]*\)', '', x.replace(" (page does not exist)", "")).encode('utf-8'))
			print uclean
			m[uclean] = tab
			return m
		return False

	def urlLastPart(self):
		ind = (self.url.rindex("/") + 1)
		u = self.url[ind:].encode('utf-8').replace("_", " ")
		return u
