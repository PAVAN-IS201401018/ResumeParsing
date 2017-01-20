from careerjet_api_client import CareerjetAPIClient
import MySQLdb as mysql



def similarity(text1, text2):
	s1 = set(text1.split())
	s2 = set(text2.split())
	un = s1.union(s2)
	intersect= s1.intersection(s2)
	return ( len(intersect) *1.0 )/ ( len(un) *1.0 )

def crawl():	
	cj  =  CareerjetAPIClient("en_GB")
	result_json = cj.search({'location':'london', 
		'affid':'15dab4607182f9977616ac6edc0ddd75',
		'user_ip':'192.168.1.64', 
		'user_agent':'Mozilla/5.0 (X11; Linux x86_64; rv:31.0) Gecko/20100101 Firefox/31.0', 
		'url':'http://www.example.com/jobsearch?q=python&l=london'})
	jobs = result_json['jobs']
	db = mysql.connect(host="localhost", user="root", passwd="iiits_12345", db="onet")        
	cur = db.cursor()
	cur.execute("""SELECT title, description ,onetsoc_code FROM occupation_data """)	

	RI = []
	db_results = cur.fetchall()
	for j in range(len(jobs)):
		RI.append([]) 
		title =  str(jobs[j]['title'].encode('utf8'))
		description  = str(jobs[j]['description'].encode('utf8'))

		for _c in range(len(db_results)):
			onet_title = db_results[_c][0]  
			onet_desc = db_results[_c][1]
			onet_code = db_results[_c][2]
			cur.execute("""SELECT alternate_title, short_title from alternate_titles WHERE onetsoc_code = """ + "'"+str(onet_code)+"'")
			alter = cur.fetchall();
			bias = 0.0
			for a in alter:
				tbias = similarity(title, a[0]) 
				if a[1] != None:
					tbias += similarity(title, a[1])
				bias = max(tbias, bias)
								
			score = bias + similarity(title,onet_title )+ 0.5*similarity(title, onet_desc)+0.5*similarity(description, onet_title) + 0.1*similarity(description, onet_desc)
	       		RI[j].append(tuple([onet_code, onet_title, score]))
	
		RI[j] = tuple([title,sorted(RI[j], key=lambda x: x[2], reverse=True)])

	for r in RI:
		print "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
		print r[0]
		for x in r[1][:10]:
			print x
			print "---------------------------------------------------------------"
	return RI		

c = crawl()	
