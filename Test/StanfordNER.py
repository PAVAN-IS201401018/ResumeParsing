# -*- coding: utf-8 -*-
# working code
from docx import Document
import copy
import re
from os import listdir
from os.path import isfile, join

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO
import nltk
import os , sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
from nltk import pos_tag
from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize
from nltk.chunk import conlltags2tree
from nltk.tree import Tree
from setuptools import setup
import sys

#reload(sys)
#sys.setdefaultencoding('utf8')

style.use('fivethirtyeight')


def process_text():
    
    text1 = open("/home/pavan/abc.txt").read()
    text2=text1.decode('utf-8','ignore')
    token_text = word_tokenize(text2)
    return token_text

# Stanford NER tagger    
def stanford_tagger(token_text):
	st = StanfordNERTagger('/home/pavan/Downloads/stanford-ner/classifiers/english.all.3class.distsim.crf.ser.gz',
							'/home/pavan/Downloads/stanford-ner/stanford-ner.jar',
							encoding='utf-8')   
	ne_tagged = st.tag(token_text)
	return(ne_tagged)
 
# NLTK POS and NER taggers   
def nltk_tagger(token_text):
	tagged_words = nltk.pos_tag(token_text)
	ne_tagged = nltk.ne_chunk(tagged_words)
	return(ne_tagged)

# Tag tokens with standard NLP BIO tags
def bio_tagger(ne_tagged):
		bio_tagged = []
		prev_tag = "O"
		for token, tag in ne_tagged:
			if tag == "O": #O
				bio_tagged.append((token, tag))
				prev_tag = tag
				continue
			if tag != "O" and prev_tag == "O": # Begin NE
				bio_tagged.append((token, "B-"+tag))
				prev_tag = tag
			elif prev_tag != "O" and prev_tag == tag: # Inside NE
				bio_tagged.append((token, "I-"+tag))
				prev_tag = tag
			elif prev_tag != "O" and prev_tag != tag: # Adjacent NE
				bio_tagged.append((token, "B-"+tag))
				prev_tag = tag
		return bio_tagged


# Create tree       
def stanford_tree(bio_tagged):
	tokens, ne_tags = zip(*bio_tagged)
	pos_tags = [pos for token, pos in pos_tag(tokens)]

	conlltags = [(token, pos, ne) for token, pos, ne in zip(tokens, pos_tags, ne_tags)]
	ne_tree = conlltags2tree(conlltags)
	return ne_tree


# Parse named entities from tree
def structure_ne(ne_tree):
	ne = []
	for subtree in ne_tree:
		if type(subtree) == Tree: # If subtree is a noun chunk, i.e. NE != "O"
			ne_label = subtree.label()
			ne_string = " ".join([token for token, pos in subtree.leaves()])
			ne.append((ne_string, ne_label))
	return ne

def stanford_main():
	a1=structure_ne(stanford_tree(bio_tagger(stanford_tagger(process_text()))))
	print a1
def nltk_main():
	a2=structure_ne(nltk_tagger(process_text()))



if __name__ == '__main__':
	stanford_main()
	nltk_main()
