import codecs
import operator
d={}
i=0
thresh=10000



def findcats(thresh, topncats=False, n=50, verbose=True, etype="Tmall"):
 d={}
 i=0
 with codecs.open("data/JD_Tmall_4to10.csv", encoding="gbk") as fh:
   for line in fh:
     if line.split(",")[3]==etype:
       tmp = line.split(",")[4]
       d[tmp]=d.get(tmp,0)+1
     i+=1
     if i>thresh: break
   #print i  ## Prints the number of iterations made searching the file

 if verbose==True:
   for k,v in d.items():
     print k,v
 if topncats==True: d=dict(sorted(d.items(), key=operator.itemgetter(1),reverse=True)[:n])
 return d




def cattocsv(catstr):
 ## param catstr can be a string or list of strings
 test_cat = []
# if type(cats)==type(""): cats = list(cats)
# if type(cats)==type([]): 
 with codecs.open("data/JD_Tmall_4to10.csv", encoding="gbk") as fh:
  for line in fh:
   if line.split(",")[4]==catstr: test_cat.append(line)
 with codecs.open("data/"+catstr+".csv", "w", encoding="gbk") as fh:
  for line in test_cat:
   fh.write(line)
 