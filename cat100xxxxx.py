import codecs
import operator
import pandas as pd

d={}
i=0
thresh=10000



def get50Categories(**kwargs):
    """ Returns a list of 50 DataFrames for analysis, representing a category/reference month
    
        optional: pass argument ref_date_i = 0,1,2,3,4 or 5 
    """
    
    catcounts  = findcats(1e7, topncats=True, verbose=False)
    categories = sorted(catcounts.keys())
    return [readCategory(categories[i],**kwargs) for i in range(len(categories))]


def findcats(thresh, topncats=False, n=50, verbose=True, etype="Tmall"):
 d={}
 i=0
 with codecs.open("../data/JD_Tmall_4to10.csv", encoding="gbk") as fh:
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


def readCategory(catstr, ref_date_i=4):  ##ref_date_i is in [0,5]
    """ Returns a dataframe for a given category/ref_date
    """

    if ref_date_i not in range(6): raise AttributeError("ref_date_i must be in [0, 5]")
    df = pd.read_csv("../data/"+catstr+".csv", names=["egoodsid","c30","q30","etype","catid","fenlei","ref_date"])
    df = df[df.q30.notnull()]
    df["ratio"] = df.c30/df.q30
    df = df[(df.ref_date==20160501+ref_date_i*100)&(df.ratio<1)]
    return df


def cattocsv(catstr):
 ## param catstr can be a string or list of strings
 test_cat = []
# if type(cats)==type(""): cats = list(cats)
# if type(cats)==type([]): 
 with codecs.open("../data/JD_Tmall_4to10.csv", encoding="gbk") as fh:
  for line in fh:
   if line.split(",")[4]==catstr: test_cat.append(line)
 with codecs.open("data/"+catstr+".csv", "w", encoding="gbk") as fh:
  for line in test_cat:
   fh.write(line)
 
   