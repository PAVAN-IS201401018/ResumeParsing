from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO

def convert_pdf_to_txt():
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = file('my.pdf', 'rb')
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

k=convert_pdf_to_txt()
p=k.split('\n')
m=[]
c=0
list=['python','java','c','programming','c++','databases','mysql','r','shell scripting','django','ms office','ms-office']
for p1 in p:
	if p1:
		a=p1.split(' ')
		for i in a:
			op=i.lower()
			m.append(op)
print m
for i in list:
	
	if i in m:
		c=c+1
print str(c)+"/"+str(len(list))
