from bs4 import BeautifulSoup
import re

class Parser:
	def __init__(self, content, url):
		self.content = content
		self.url = url
	
	def cleanAndRun(self):
		if(self.cleaner()):
			return self.parse()
	
	## the first page remove the top and the bottom of the page 
	## in order to have only the keywords list
	## the second part remove all the unwanted strings
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

		self.content = self.content.replace(" (page does not exist)", "")
		self.content = re.sub(r' \([^)]*\)', '', self.content)
		try:
			self.content = self.content[:min(pEnd)]
		except:
			return False
		return True

	## parse the list of keywords and do some more cleaning
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
		if(self.isBadTitle(uclean) == False):
			for x in data:
				if x.find(":") == -1 and (self.isBadKeyword(x) == False) and (self.isCountry(x) == False) and x != uclean:
					tab.append(x.encode('utf8'))
			print uclean
			m[uclean] = tab
			if (len(tab) > 0):
				return m
		return False

	## parse the url for the key
	def urlLastPart(self):
		ind = (self.url.rindex("/") + 1)
		u = self.url[ind:].encode('utf-8').replace("_", " ")
		return u


	def isBadTitle(self, title):
                title = title.lower()
                title_list = ["additives", "people", "wiki", "wikipedia", "brand", "military"]
                return any(substring in title for substring in title_list)

	## check if the potential keyword contains a bad keyword
	def isBadKeyword(self, keyword):
		keyword = keyword.lower()
		keyword_list = ["lists of", "list of", "cuisine", "people", "index", "revolution", "farming", "agriculture", "ecology", "ecologic","engineering", "agricultural", "international", "standart", "new york", "history", "renaissance", "manhattan", "geographical", "specialties", "specialty", "commission", "book", "recipe", "nomenclature", "explosion", "illustration", "stadium", "kit", "combat", "war ", "military", "armed", "forces", "island", "punishment", "world", "law ", "civil", "death", "prisoner", "christmas", "game", "preservation", "latin", "islam", "muhammad", "reproduction", "sex", "sexual", "asexual", "discussion", "article", "page", "[", "civilization", "h5n1", "origin", "constitution", "jewish", "islamic", "teenage", "ninja", "pirates", "factory", "christian", "colonization", "street", "act", "blackberry", "android", "samsung", "google", "pixar", "disney", "family", "superman", "captain", "g.i.", "mr.", "e.t.", "general", "monster", "wedding", "merveilleux", "north", "insects", "uncle", "national", "academy", "academies", "lore ", "diet ", "word", "adam", "aquaculture", "district", "municipality", "instant", "microbiology", "fermentation", "guides", "guide", "wikipedia", "account", "mandatory", "language", "restaurant", "children"]
		return any(substring in keyword for substring in keyword_list)

	## check if the keyword contains a country name
	def isCountry(self, keyword):
		country_list = ["Afghanistan","Albania","Algeria","America","Andorra","Angola","Anguilla","Antigua &amp; Barbuda","Argentina","Armenia","Aruba","Australia","Austria","Azerbaijan","Bahamas","Bahrain","Bangladesh","Barbados","Belarus","Belgium","Belize","Benin","Bermuda","Bhutan","Bolivia","Bosnia &amp; Herzegovina","Botswana","Brazil","British Virgin Islands","Brunei","Bulgaria","Burkina Faso","Burundi","Canada","Cambodia","Cameroon","Cape Verde","Cayman Islands","Chad","Chile","China","Colombia","Congo","Cook Islands","Costa Rica","Cote D Ivoire","Croatia","Cruise Ship","Cuba","Cyprus","Czech Republic","Denmark","Djibouti","Dominica","Dominican Republic","Ecuador","Egypt","El Salvador","Equatorial Guinea","Estonia","Ethiopia","Falkland Islands","Faroe Islands","Fiji","Finland","France","French Polynesia","French West Indies","Gabon","Gambia","Georgia","Germany","Ghana","Gibraltar","Greece","Greenland","Grenada","Guam","Guatemala","Guernsey","Guinea","Guinea Bissau","Guyana","Haiti","Honduras","Hong Kong","Hungary","Iceland","India","Indonesia","Iran","Iraq","Ireland","Isle of Man","Israel","Italy","Jamaica","Japan","Jersey","Jordan","Kazakhstan","Kenya","Kuwait","Kyrgyz Republic","Laos","Latvia","Lebanon","Lesotho","Liberia","Libya","Liechtenstein","Lithuania","Luxembourg","Macau","Macedonia","Madagascar","Malawi","Malaysia","Maldives","Mali","Malta","Mauritania","Mauritius","Mexico","Moldova","Monaco","Mongolia","Montenegro","Montserrat","Morocco","Mozambique","Namibia","Nepal","Netherlands","Netherlands Antilles","New Caledonia","New Zealand","Nicaragua","Niger","Nigeria","Norway","Oman","Pakistan","Palestine","Panama","Papua New Guinea","Paraguay","Peru","Philippines","Poland","Portugal","Puerto Rico","Qatar","Reunion","Romania","Russia","Rwanda","Saint Pierre &amp; Miquelon","Samoa","San Marino","Satellite","Saudi Arabia","Senegal","Serbia","Seychelles","Sierra Leone","Singapore","Slovakia","Slovenia","South Africa","South Korea","Spain","Sri Lanka","St Kitts &amp; Nevis","St Lucia","St Vincent","St. Lucia","Sudan","Suriname","Swaziland","Sweden","Switzerland","Syria","Taiwan","Tajikistan","Tanzania","Thailand","Timor L'Este","Togo","Tonga","Trinidad &amp; Tobago","Tunisia","Turkey","Turkmenistan","Turks &amp; Caicos","Uganda","Ukraine","United Arab Emirates","United Kingdom","Uruguay","Uzbekistan","Venezuela","Vietnam","Virgin Islands (US)","Yemen","Zambia","Zimbabwe", "United States"];
		return any(substring in keyword for substring in country_list)
