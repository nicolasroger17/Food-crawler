from Crawler import *

print "procesing..."
f = open("output.json", 'w')
f.write('{\n\t"data" : {\n')
f.close()

crawler = Crawler("http://en.wikipedia.org/wiki/Category:Lists_of_foods")
crawler.parseForLinks()

f = open("output.json", 'a')
f.write('\t}\n}')
f.close()
print "done"
