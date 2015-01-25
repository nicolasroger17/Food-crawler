from Crawler import *

print "procesing..."
##crawler = Crawler("http://en.wikipedia.org/wiki/Category:Lists_of_foods")
##crawler.parseForLinks()
f = open('input.txt').read()
parser = Parser(str(f))
parser.cleaner()
parser.parse()
print "done"
