import codecs
import operator
import pandas as pd
from matplotlib import pylab as py
from scipy.stats import beta as betadist

#haow to use?
#1.import query100xxxxx as que
#2.def catstr=[],thresh=90000,toprange=47 before use the functions


def runEverything(numofcats=10, ref_date="20160601", c=140, thresh=100000):


    catstr   = findcats(thresh, numofcats)
    test_cat = takecat(catstr, ref_date)
    TC       = cleancat(test_cat) 
    dfpe      = toevan(TC, catstr, int(ref_date), c)
    return dfpe

def findcats(thresh,toprange):
    
    d={}
    i=0
    catstr=[]
    with codecs.open("JD_Tmall_4to10.csv", encoding="gbk") as fh:
        for line in fh:
            if line.split(",")[3]==u"Tmall":
                tmp = line.split(",")[4]
                d[tmp]=d.get(tmp,0)+1
            i+=1
            if i>thresh: break
        sort_d = sorted(d.items(), key=operator.itemgetter(1),reverse=True)
        #print sort_d
        
        for i in range(toprange):
            tup = sort_d[i]
            catstr.append(tup[0])
        
        return catstr
 


   
def takecat(catstr,ref_date):
    test_cat = []
    with codecs.open("JD_Tmall_4to10.csv", encoding="gbk") as fh:
        for line in fh:
            if line.split(",")[4] in catstr and line.split(",")[6][:-2]==ref_date: #delete \r\n at the end of one line
                test_cat.append(line)
        #with open(catstr[k]+".csv", "w") as fh:
        #    for line in test_cat:
        #        fh.write(line)

    
    return test_cat
                

def cleancat(test_cat):
    egoodsid = []
    c30 = []
    q30 = []
    etype = []
    categoryid = []
    fenlei = []
    ref_date = []
    
    for line in test_cat:
        egoodsid.append(line.split(",")[0])
        
        tmp = line.split(",")[1]
        if tmp=='':c30.append(0)
        else:c30.append(int(tmp))
            
        tmp = line.split(",")[2]
        if tmp=='':q30.append(0)
        else:q30.append(int(tmp))
            
        etype.append(line.split(",")[3])
        categoryid.append(line.split(",")[4])
        fenlei.append(line.split(",")[5])
        ref_date.append(int(line.split(",")[6][:-2]))
    
    # converge lists into a dict and change this dict into a dataframe
    tc = {"egoodsid":egoodsid,"c30":c30,"q30":q30,"etype":etype,"categoryid":categoryid,"fenlei":fenlei,"ref_date":ref_date}
    TC = pd.DataFrame(data=tc)
    
    TC = TC.drop("fenlei", axis=1)
    TC = TC[TC["q30"]!=0]
    TC["ratio"] = TC.c30/TC.q30
    
    return TC
    
    
    
    
    
def toevan(TC,catstr,ref_date, c=140):
    pes = []
    Ms  = []
    q30acts= []
    q30ests= []
    for i in range(len(catstr)):

        q30totalact = TC[(TC["categoryid"]==catstr[i])&(TC["ref_date"]==ref_date)&(TC["c30"]!=0)].q30.sum()
        M = len(TC[(TC["categoryid"]==catstr[i])&(TC["ref_date"]==ref_date)&(TC["c30"]!=0)])
#        if M==0:continue
            
        if M < 18:continue
            
        a = betadist.fit(TC[(TC.categoryid==catstr[i])&(TC["ref_date"]==ref_date)&(TC["c30"]!=0)&(TC["ratio"]<1)]["ratio"], floc=0, fscale=1)
        EV = a[0]/(a[0]+a[1])
        con = EV*c*0.001
        try: cce = sum(py.divide(TC[(TC.categoryid==catstr[i])&(TC["ref_date"]==ref_date)&(TC["c30"]!=0)].sort_values(by="c30", ascending=False).c30.tolist(),con*py.log(range(2,M+2))))
        except: cce = sum(TC[(TC.categoryid==catstr[i])&(TC["ref_date"]==ref_date)&(TC["c30"]!=0)].sort_values(by="c30", ascending=False).c30.tolist()/con*py.log(range(2,M+1)))
            
        pes.append(100*(cce-q30totalact)/q30totalact)
        Ms.append(M)
        q30acts.append(q30totalact)
        q30ests.append(cce)

        
    return pd.DataFrame({"pe":pes,"M":Ms,"q30act":q30acts,"q30est":q30ests})
    #py.hist(pes)
    #to_minimize = [sum(map(abs,[pes[i][k] for i in range(3)])) for k in range(120)]#need toprange instead of number 3
    #py.plot(range(125-60,125+60),to_minimize,"g")
    #py.plot([to_minimize.index(min(to_minimize))+125-60,to_minimize.index(min(to_minimize))+125-60],[-200,400], "r:")
    #py.xlim(60,200);py.ylim(-100,200)
    
    #pe1 = index(min(to_minimize)
    
    
                
    