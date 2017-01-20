from rules.generic.SectionTitles import section_titles, section_titles_list
from rules.it_programmer import gazette
from rules.it_programmer.tags import stack_tags #type:list()
from pprint import pprint
from nltk.data import load as nltk_data_load
from nltk.tokenize import word_tokenize
from nltk.tag import StanfordPOSTagger
from nltk.tag import StanfordNERTagger
from nltk.tag import pos_tag
from nltk.corpus import wordnet as wn
from nltk import FreqDist
from sklearn import svm
import numpy as np
import matplotlib.pyplot as plt
import sys
import nltk
import re
import math
import os
#Escaping UnicodeDecodeEncode Errors.
#reload(sys)
#sys.setdefaultencoding('utf8')

def findkey(string, regList):
	'''
	Regex based Keyfinder for a python dict.
	'''
	for r in regList:
		if re.search(r, string) != None:
			return r 
	return None	

def get__dict__(lst):

	'''
	Input type: list(str)
	Function: Uses the generic resume parsing rules from
		rules.generic and parses the input resume
		list of raw text to a python dict of categorical
		data.
    	A generic example output format would be:
		{'summary':'to seek a career as software developer',
		 'courses':'data structures, algorithms',
		 'skills':'redis, mysql',
		 ....
		 ....
		 'education and training':'stanford univesity bs in computer science'
		}

	Output type: Dictionary.		  	
	'''
	regex1 = re.compile(r"^\\u?[0-9]?[0-9]?[0-9]?[a-zA-Z]$", re.IGNORECASE)
	regex2 = re.compile(r"^0x?[a-zA-Z]?[0-9]$", re.IGNORECASE)
	regex3 = re.compile(r"^\\x?[a-zA-Z0-9]?[0-9a-zA-Z]$", re.IGNORECASE)

	D = dict()
	
	lst = list(filter(lambda x: x != '\n' , lst))
	
	lst = map(lambda x: re.sub(regex1,'',
		 re.sub(regex2,'',
		 re.sub(regex3, '', x.strip().strip(':')
		.replace('\xe2\x80\x93','-')
		.replace('_-_','-')
		.replace('\xe2\x80\xa2','')
		.replace('\xe2\x80\x99','')
		.replace('\xef\x82\xb7','')
		.replace('\u201c','')
		.replace('0xe2','')
		.strip()
		.lower()))),
		lst)


	key = None
	
	for y in lst:
		dkey = section_titles.keys()
		if  y in dkey:
			key = section_titles[y]
		elif key != None:
			try:
				D[key]+= " " + y
			except KeyError:
				D[key] = y			

	return D

def is_subset(string1, string2):
	'''
	Assumes string2.length  > string1.length
	Returns if string1 subset or equal to string2
	'''	
	s1,s2 = [len(string1),len(string2)]
	for x in range(s1):
		if s2 < s1:
			return False
		elif string1[x] != string2[x]:
			return False
	return True		

def get_sentences(text):

	'''
	Input type: str
	Function: Given a text, detects sentence boundaries
			  and tokenizes the text into sentences.
	Output type: list(str)
	'''

	sentence_detector = nltk_data_load('tokenizers/punkt/english.pickle')	

	return sentence_detector.tokenize()

def wordnet_similar_nouns(word):
    
    '''
    Noun-Word Association using Wordnet
    Given a word, retrieves all similar / related nouns .  
    This is used to identify words that does not include
    in resume or job posting but are associated with words 
    that are present in the job posting.
    '''
    nouns = list()
    wn_synsets = wn.synsets(word, pos=wn.NOUN)

    for wd in wn_synsets:
    	wd_lemmas = wn.synset(wd.name()).lemmas()
    
    	for wl in wd_lemmas:
    		nouns.append(wl.name().replace('_',' ')) 
    
    return list(set(nouns))

def wordnet_similar_verbs(word): 

    '''
    Given a verb, retrieves all similar / related verbs .
    This is used to identify words that does not include
    in resume or job posting but are associated with words 
    that are present in the job posting.
    '''
    verbs = list()
    wn_synsets = wn.synsets(word, pos=wn.VERB)

    for wd in wn_synsets:
    	wd_lemmas = wn.synset(wd.name()).lemmas()
    
    	for wl in wd_lemmas:
    		verbs.append(wl.name().replace('_',' ')) 
    
    return list(set(verbs))	

def nltk_tagger(data_dict):
	
	'''
	Input: A python dictionary with section title (key) and section values( values ).

	Function: Uses nltk library to perform parts of speech tagging to identify nouns 
			  and verbs in the text.

	Output: A python dict with section title (key) and tuple containing two lists: 
			[Named Entities Identified, Task Entities Identified].
	'''
	TAGGED = {}
	dkeys = data_dict.keys()

	for section in dkeys:

		TAGGED[section] = {
			#Verbs
			'VERB':[],
			#Named Entity Recognition Tuples
			'NERT':[],
			#Nouns
			'NOUN':[]
		}

		data = data_dict.get(section)

		tokenized = nltk.tokenize.word_tokenize(data)
		tokenized = map(lambda Z: Z.lower(), tokenized )

		#spt_model = 'english-bidirectional-distsim.tagger'
		#spt = StanfordPOSTagger(spt_model)
		
		#snert_model = 'english.all.3class.distsim.crf.ser.gz'
		#snert = StanfordNERTagger(snert_model)

		#nert_tagged = snert.tag(data)
		#pos_tagged = spt.tag(data)
		pos_tagged = pos_tag(tokenized)

		verbs = list()
		
		for x in pos_tagged:
			if x[1].startswith('VB'):
				verbs.append(x[0])
				wn_verbs = wordnet_similar_verbs(x[0])

				for v in wn_verbs:
					verbs.append(v)

		nouns = list()
		
		for x in pos_tagged:
			if x[1].startswith('NN'):
				nouns.append(str(x[0]))
				wn_nouns = wordnet_similar_nouns(x[0])
				for n in wn_nouns:
					nouns.append(n)
		
		#nert = filter(lambda X: X[1] != 'O', nert_tagged)
		
		TAGGED[section]['VERB'] = verbs
		TAGGED[section]['NOUN'] = nouns
		#TAGGED[section]['NERT'] = nert		

	return TAGGED

def bigrams(input_list):
	return zip(input_list, input_list[1:])
def trigrams(input_list):
	return zip(input_list, input_list[1:], input_list[2:])	

def grams(f):

	'''
	Return Format : list() 
	'''
	b_o_w = []
	with open(f) as fp:
		L = fp.read()

	tokens = L.split()
	tokens = map(lambda Z: Z.lower(), tokens )
	#Gazette based.

	'''
	for t in tokens:
		for regex in gazette.gazette.get('indexes').keys():
			if re.search("^"+regex+"$", t.lower().strip(',')) != None:
				
				b_o_w.append(t)
	'''			
	# StackOverFlow Tag based NER
	
			
	return [tokens, bigrams(tokens), trigrams(tokens)]


def bulk_bag_of_words(path):

	'''
	'''
	bulk = list()
	list_files = os.listdir(path)
	list_files = list(set(map(lambda Z: (path+Z).strip('~'), list_files)))
	count_of_files = len(list_files)
	for _f in range(count_of_files):
		f = list_files[_f]
		#print("Building bag of words.. File %s of %s" % (str(_f+1),count_of_files))
		g = grams(f)
		bulk.append({'uni':g[0], 'bi':g[1], 'tri':g[2]})
	return bulk

def get_similar(r,p):

	'''
	Get the tokens that are similar to all the words
	Returns a dict with Frequency Distribution split as resume and posting
	'''
	rsim = list()
	psim = list()
	for _r in r:
		pkey = findkey(_r, gazette.gazette['indexes'])
		gsim = gazette.gazette.get('indexes').get(pkey).get('similar')
		rsim += gsim
	for _p in p:
		pkey = findkey(_p, gazette.gazette['indexes'])
		gsim = gazette.gazette.get('indexes').get(pkey).get('similar')	 
		psim += gsim
	return {'r':FreqDist(rsim), 'p':FreqDist(psim)}	

def get_related(r,p):
	
	'''
	Get the tokens that are related to all the words
	Returns a dict with Frequency Distribution split as resume and posting
	'''
	rrel = list()
	prel = list()
	for _r in r:
		pkey = findkey(_r, gazette.gazette['indexes'])
		grel = gazette.gazette.get('indexes').get(pkey).get('similar')
		rrel += grel
	for _p in p:
		pkey = findkey(_p, gazette.gazette['indexes'])
		grel = gazette.gazette.get('indexes').get(pkey).get('similar')	 
		prel += grel
	return {'r':FreqDist(rrel), 'p':FreqDist(prel)}	
 

def get_common(r,p):
	
	'''
	count of words common in resume, posting
	Input types - r:list, p:list
	return type - int
	'''
	return len(set(p).intersection(set(r)))

def get_domain_dist_freq(r,p):	

	'''
	Input type - r:list, p:list
	Calculates the ratio of domains Frequency in posting to resume({ d E postings.domains }).
	Output type - float
	'''
	pdomains = list()
	for _p in p:
		pkey = findkey(_p, gazette.gazette['indexes'])
		domain = gazette.gazette.get('indexes').get(pkey).get('domain')
		pdomains += domain 		
			
	rdomains = list()	
	for _r in r:
		pkey = findkey(_r, gazette.gazette['indexes'])
		rd = gazette.gazette.get('indexes').get(pkey).get('domain')
		for _rd in rd:
			if _rd in pdomains:
				rdomains.append(_rd) 	
	try:
		score = len(rdomains)*1.0 / len(pdomains)*1.0
	except ZeroDivisionError:
		score = 0.0	
	return score

def similar_cosine(F):
	
	'''
	'''
	r = F['r']
	p = F['p']
	A = r
	B = p
	for _r in r:
		if _r not in B.keys():
			B[_r] = 0

	for _p in p:
		if _p not in A.keys():
			A[_p] = 0
	return cosine_similarity(A, B, len(A))

def related_cosine(F):

	'''
	'''
	r = F['r']
	p = F['p']
	A = r
	B = p
	for _r in r:
		if _r not in B.keys():
			B[_r] = 0

	for _p in p:
		if _p not in A.keys():
			A[_p] = 0
	return cosine_similarity(A, B, len(A))

def build_cosine_vector(r,p):
	R = {}
	P = {}
	
	for _r in r:
		if type(_r) != type("str"):
			_r = " ".join(_r)
		try:
			R[_r]+=1	
		except KeyError:
			R[_r] = 1
		
		if _r not in p:
			P[_r] = 0

	for _p in p:
		if type(_p) != type("str"):
			_p = " ".join(_p)
		try:
			P[_p] += 1
		except KeyError:
			P[_p]=1	
		if _p not in r:
			R[_p]=0

	return [R,P]	

def cosine_similarity(RP):
	
	'''
	'''
	nume =  0.0
	deno_a = 0.0
	deno_b = 0.0
	R = RP[0]
	P = RP[1]
	for i in R:
		nume += R[i]*P[i]
		deno_a += R[i]*R[i]
		deno_b += P[i]*P[i]
	try:
		cosine_score = nume / (math.sqrt(deno_a) * math.sqrt(deno_b))		
	except ZeroDivisionError:
		cosine_score = 0.0
	return cosine_score

			
def feature_space_row(r, p):
	
	'''
	'''
	'''
	fsr = [get_domain_dist_freq(r['bow'], p['bow']), 
				 get_common(r['bow'],p['bow']), 
				 similar_cosine(get_similar(r['bow'],p['bow'])), 
				 related_cosine(get_related(r['bow'],p['bow']))]
	'''
	fsr = [cosine_similarity(build_cosine_vector(r['uni'],p['uni'])),
		   cosine_similarity(build_cosine_vector(r['bi'],p['bi'])),
		   cosine_similarity(build_cosine_vector(r['tri'],p['tri'])),
		   get_common(r['uni'],p['uni']), 
		   get_common(r['bi'],p['bi']),
		   get_common(r['tri'],p['tri']),
		   len(r['uni']), 
		   len(p['uni'])]
	
	return fsr

def label_input(FEATURE_SPACE):
	
	'''
	'''
	LABELLED = list()
	counter = 1

	for f in FEATURE_SPACE:
		_f1 = f[0] 
		_f2 = f[1]
		_f3 = f[2]
		_f4 = f[3]
		lbl = raw_input('Provide label for %d: \nR - Relevant \tN-Not Relevant\n' % (counter)).strip()
		counter += 1
		LABELLED.append([_f1,_f2, _f3, _f4, lbl])

	return LABELLED

def label_input_score(FEATURE_SPACE):
	
	'''
	'''
	SCORED = list()

	cardinality = len(FEATURE_SPACE)

	for x in range(cardinality):
		try:

			SCORED.append( tuple(FEATURE_SPACE[x]))
		
		except TypeError:
			pass

	return SCORED

def build_feature_space(R,P):

	'''
	'''

	fs = list()
	counter = 0

	for r in R:
		fs.append(feature_space_row(r,P))

	return label_input_score(fs)		

def train_set_testset(LABELLED_FEATURE_SPACE):
	
	'''
	Divides a given feature space vector in two parts : Train and Test
	Division of Train set and Test set are done as in halfs to avoid
	-	neither of them becoming overly large than the other leading to lower accuracy.
	'''

	L = len(LABELLED_FEATURE_SPACE)
	L_mid = L/2

	return {'train':LABELLED_FEATURE_SPACE[:L_mid], 'test':LABELLED_FEATURE_SPACE[L_mid:]}

def training_classifier(train_set, labels):

	'''
	'''
	#Performs naive bayes classification based on nltk and returns a trained classifier instance
	classifier = svm.SVC().fit(train_set, labels)

	return classifier

def test_classify(classifier, test_set):

	'''
	'''
	return classifier.predict(test_set)

def resume_rank(RANKS):
	return sorted(RANKS, key=lambda A: A[1], reverse=True)


def plot_graph(clfr,clfd):
	x_min, x_max = 0, 10
	y_min, y_max = 0, 10
	h = .02
	xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                     np.arange(y_min, y_max, h))
	Z = clfd

 	# Put the result into a color plot
    	Z = Z.reshape(xx.shape)
    	plt.contourf(xx, yy, Z, cmap=plt.cm.coolwarm, alpha=0.8)
	plt.show()
