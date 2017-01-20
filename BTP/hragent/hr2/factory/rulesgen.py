import sys
import os
from pprint import pprint
import json
# Read rule headers
# List them all to user
# Take options
# Store in dict
# Write to file

def display(lst):
	nb = 1
	for y in lst:
		print "%d. %s" %(nb,y)
		nb += 1

def populate(dct, dom, raw):
	for x in raw:
		try:
			dct["indexes"][x]["related"]= list()
		except KeyError:
			dct["indexes"][x] = {"related":[],"domain":[],"similar":[]}
	return dct

# Execution starts here.
BASE_DIR = os.getcwd()
I_FILE = "%s/input" % (BASE_DIR) 
D_FILE = "%s/domains" % (BASE_DIR)
O_FILE = "%s/rules" % (BASE_DIR)

inf = open(I_FILE,"rb")
dmf = open(D_FILE,"rb")

raw = sorted(map(lambda Z: Z.strip(), inf.readlines()))
dom = sorted(map(lambda Z: Z.strip(), dmf.readlines()))
inf.close()
dmf.close()
GAZETTE = json.load(open("gazette.json","r"))
GAZETTE = populate(GAZETTE, dom, raw)
print "imported existing gazette"
pprint(GAZETTE)
#populate(GAZETTE, dom, raw)
#30 - 35 not yet entered!
for _x in range(30,31):#len(raw)):
	x = raw[_x]
	print ":::::::::: %d :::::::::" % (_x + 1)

	x_xclude = filter(lambda Z: Z!= x, raw) 
	
	display(dom)
	print "Select Domains for %s" % (x)
	
	I = raw_input().split()
	
	if I[0] == "jump":
		_x = int(I[1]) - 1

	else:	 
		_g = map(lambda Z: dom[int(Z)-1], I)
		print _g
		g = GAZETTE["indexes"][x]["domain"]
		
		updated = list(set(g + _g))
		GAZETTE["indexes"][x]["domain"] = updated 	
	
		print "-----------------------------------------------------"
		print "Domains for ", x , ": ", "  ", updated
	print "-----------------------------------------------------"

	display(x_xclude)
	print "Select SIMILAR for %s" % (x)
	
	I = raw_input().split()
	
	_g = map(lambda Z: x_xclude[int(Z)-1], I)
	g = GAZETTE["indexes"][x]["similar"]

	updated = list(set(g + _g))
	GAZETTE["indexes"][x]["similar"] = updated 

	print "-----------------------------------------------------"

	display(x_xclude)
	print "Select related for %s" % (x)
	
	I = raw_input().split()
	
	_g = map(lambda Z: x_xclude[int(Z)-1], I)
	g = GAZETTE["indexes"][x]["related"]

	updated = list(set(g + _g))
	GAZETTE["indexes"][x]["related"] = updated 
	with open("gazette.json", "w") as j:
		json.dump(GAZETTE,j)


'''
with open("gazette.json", "w") as j:
	pprint(json.dumps(GAZETTE),j)
'''
 	