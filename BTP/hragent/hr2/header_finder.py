import os

def read_and_merge_headers(path, to_merge):
	d = open(path, "r+")
	h = d.readline().split("$")
	h = h + to_merge
	h = list(set(h))
	st = "$".join(h)
	d.write(st)
	d.close()

def final_print(path):
	d = open(path, "r+")
	h = d.readline().split("$")
	for x in h:
		d.write(x)
		d.write("\n")
	d.close()	

def get_headers(path):
	headers = list()
	d = open(path, "rb")
	sections = d.readlines()
	
	for x in sections:
		_x = x.split()
		if len(_x) > 0 and len(_x) < 4:
			headers.append(x.lower())
	return headers

BASE_DIR = os.getcwd()+"/output/"
files = os.listdir(BASE_DIR)
for f in files:
	path = "%s/%s" % (BASE_DIR,f)
	hf = get_headers(path)
	read_and_merge_headers(BASE_DIR+"headers.txt",hf)		
final_print(path)	