from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import HTMLConverter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from nltk.tokenize import word_tokenize
from cStringIO import StringIO
from rules.generic.headers import section_titles_tree as st
from pprint import pprint
from resume import get__dict__
from resume import nltk_tagger

import re
import csv
import os
import json


def fn_format(n):
    
    '''
    Beautifies numbering. 
    '''
	
    if n/10 == 0:
	return "0%s" % (str(n))
        
    else: 
	return str(n)

def convert_pdf_to_html(path):
    
    '''
    Converts an input PDF format file to html code.
    '''
    
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = HTMLConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = file(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0 #is for all
    caching = True
    pagenos=set()
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)
    fp.close()
    device.close()
    string = retstr.getvalue()
    retstr.close()
    return string

def convert_pdf_to_txt(path):
    
    '''
    Produces raw text out of input pdf file.
    '''
    
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = file(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text

def preprocess(inpath, outpath):
    
    '''
    Processes all pdf files in the inpath location and produces text files 
    in outpath location after extracting raw text out of the pdf files.
    '''
    
    print "Initializing preprocessor..."
    for x in range(1,51):
	fn = fn_format(x) + ".pdf"
        print "Processing %s" % (fn)
	#rpath = "input/resumes_collected/"+fn
        rpath = inpath + fn
	#hpath = "output/%s.txt" % (fn_format(x))
        tpath = "%s/%s" % (outpath, fn_format(x))
        f = open(tpath, "w")
	f.write( convert_pdf_to_txt(rpath))
    	f.close()
	
    print "Preprocessing completed sucessfully..."

    return None  

def feature_extract_bow(BASE_DIR, PROC_DIR):
    regex1 = re.compile(r"^\\u?[0-9]?[0-9]?[0-9]?[a-zA-Z]$", re.IGNORECASE)
    regex2 = re.compile(r"^0x?[a-zA-Z]?[0-9a-zA-Z]$", re.IGNORECASE)
    regex3 = re.compile(r"^\\x?[a-zA-Z0-9]?[0-9a-zA-Z]$", re.IGNORECASE)

    
    


    files = os.listdir(BASE_DIR)
    for f in files:
        path = "%s/%s" % (BASE_DIR,f)
        p = open(path,"r")
        k = p.readlines()
        wst=""
        for x in k:
            if (x!='\n'):
                wst+= x.strip()+" "
        wst = re.sub(regex1,'',
                re.sub(regex2,'',
                re.sub(regex3, '', wst.strip().strip(':')
            .replace('\xe2\x80\x93','-')
            .replace('_-_','-')
            .replace('\xe2\x80\xa2','')
            .replace('\xe2\x80\x99','')
            .replace('\xef\x82\xb7','')
            .replace('\u201c','')
            .replace('0xe2','').
            replace(',','')
            .strip()
            .lower())))

        p.close()
        
            
        #words =  word_tokenize(str(ws))
        #wstring = " ".join(words)
        of = open("%s/%s" % (PROC_DIR, f), "w")
        of.write(wst)
        of.close()
        
    return None            

def feature_extract(BASE_DIR, PROC_DIR):

    '''
    Produce categorical output from the raw text based on resume rules.
    '''
    
    files = os.listdir(BASE_DIR)
    for f in files:
        path = "%s/%s" % (BASE_DIR,f)
        p = open(path,"r")
        k = p.readlines()
        p.close()
        dmined = get__dict__(k)
        of = open("%s/%s.json" % (PROC_DIR, f), "w")
        json.dump(dmined, of)
        
        of.close()    

def pos_nert_tag(PROC_DIR,TAGGED_DIR):
    
    '''
    Perform Parts-of-Speech and Named Entity Recognition Tagging.
    '''        

    files = os.listdir(PROC_DIR)
    files = sorted(files)
    total = len(files)
    for f in files:
        print "tagging %s of %s ..." % (f.strip('.json'), str(total))
        path = "%s/%s" % (PROC_DIR,f)
        
        with open(path) as jf:    
            data_dict = json.load(jf)

        tags = nltk_tagger(data_dict)
        of = open("%s/%s" % (TAGGED_DIR, f), "w")
        pprint(json.dumps(tags), of)
        of.close()

