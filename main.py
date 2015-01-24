from Crawler import *

print "procesing..."
crawler = Crawler("http://en.wikipedia.org/wiki/Category:Lists_of_foods")
crawler.parseForLinks()
print "done"
