from execute import preprocess, feature_extract_bow, feature_extract, pos_nert_tag

import os

inpath = "%s/input/" % (os.getcwd())
outpath = "%s/output/" % (os.getcwd())
processedpath = "%s/processed/" % (os.getcwd())
taggedpath = "%s/tagged/" % (os.getcwd())
# Uncomment preprocess if any new pdf resume is added.
print "Converting PDF to raw text..."
#preprocess(inpath, outpath)
print "Extraction from raw text: resume sections and data"
feature_extract_bow(outpath, processedpath)
print "Tagging Parts-of-Speech: Noun and Verb extraction for Vocab identification"
print "This may finish in less than a minute..."
#pos_nert_tag(processedpath, taggedpath)
#print "Check out \"tagged\" folder to see results"
