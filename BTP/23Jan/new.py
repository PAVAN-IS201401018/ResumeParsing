f=open('jobskills.txt','r')
s=[]
for line in f:
	k=line.lower()
	s.append(k)
m=[]
for i in s:
	k=i.split('\n')
	if k[0]!='':
	
		m.append(k[0])
print m
