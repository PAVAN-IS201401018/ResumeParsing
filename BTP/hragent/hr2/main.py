import os
import resume

procpath = "%s/processed/" % (os.getcwd())
postingpath = "%s/posting/text" % (os.getcwd())

print "Building bag of words for resumes" 
R = resume.bulk_bag_of_words(procpath)

print "Building bag of words for postings"
Pgrams = resume.grams(postingpath)
P = {'uni':Pgrams[0],
	  'bi':Pgrams[1],
	  'tri':Pgrams[2]	
	}

print "Preparing ML feature space"
FEATURE_SPACE = resume.build_feature_space(R,P)
with open("LABELS") as lf:
	L = map( lambda A: float(A.strip()), lf.readlines())

'''
for x in range(len(FEATURE_SPACE)):
	print ",".join(map( lambda A: str(A) , FEATURE_SPACE[x][1]))+"%s%s"%(",",L[x].strip())
'''
with open("train","r") as tf:
	train = tf.readlines()

train_set = list()
for t in train:
	train_set.append(tuple(map(lambda A: A.strip(), t.split(","))))

classifier = resume.training_classifier(train_set, L)
print "CLASSIFIED RESULTS -- RELEVANT ONES SHOWN BELOW"
test_set=FEATURE_SPACE
classified = resume.test_classify(classifier, test_set)
indiced_classified = [ tuple([x+1, classified[x]]) for x in range(len(classified))]
relevant = filter( lambda A: A[1] == 1 , indiced_classified)
print relevant
#resume.plot_graph(classifier, classified)