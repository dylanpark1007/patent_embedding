import re
import xlrd
from multiprocessing import Process, Queue
import csv
import glob
import collections
import time
import sys
import pickle
import math

import MeCab

import pickle
import math
import numpy as np
from numpy.linalg import norm
from operator import itemgetter
import MeCab
import gzip
import gensim
m = MeCab.Tagger()

def tsv():
    vocap = list(model.docvecs.doctags.keys())
    X = []
    for i in range(len(vocap)):
        X.append(model[i])
    f = open('D[아].tsv', 'w', encoding='utf-8', newline='')
    wr = csv.writer(f, delimiter='\t')
    for tag in X:
            wr.writerow(tag)
    f.close()
    # f = open('test2.tsv', 'w', encoding='utf-8', newline='')
    # wr = csv.writer(f, delimiter='\t')
    # for tag in vocap:
    #         wr.writerow(str(tag))
    # f.close()
    #
    #
    with open("T[아].tsv", "w", encoding="utf-8") as g:
        for i in range(8):
            if i>0:
                g.write("\t")
            twrd="tag"+str(i)
            g.write(twrd)
        g.write("\n")
        for i in range(len(vocap)):
            wrd=vocap[i]
            if wrd == "":
                wrd="none"
            g.write(wrd)
            g.write("\t")
            g.write(wrd[0])
            g.write("\t")
            g.write(wrd[:3])
            g.write("\t")
            g.write(wrd[:4])
            g.write("\t")
            g.write(wrd[:3])
            g.write(" ")
            if wrd[:3] in ipc_ndic:
                g.write(ipc_ndic[wrd[:3]])
            else:
                g.write("UNK")
            g.write("\t")
            g.write(wrd[:4])
            g.write(" ")
            if wrd[:4] in ipc_ndic:
                g.write(ipc_ndic[wrd[:4]])
            else:
                g.write("UNK")
            g.write("\t")
            g.write(wrd)
            g.write(" ")
            if wrd[-3:]=="/00":
                wrd=wrd.replace("/00","")
            if wrd in ipc_ndic:
                g.write(ipc_ndic[wrd])
            else:
                g.write("UNK")
            g.write("\n")
        # for tag in X:
        #     for i in range(299):
        #         g.write(str(tag[i]))
        #         g.write("\t")
        #     g.write(str(tag[299]))
        #     g.write("\n")
    return

def tsv2():
    voca = list(model.docvecs.doctags.keys())
    vocap=[wrd for wrd in voca if "/" not in wrd]
    X = []
    for i in range(len(vocap)):
        X.append(model[i])
    f = open('D[아].tsv', 'w', encoding='utf-8', newline='')
    wr = csv.writer(f, delimiter='\t')
    for tag in X:
            wr.writerow(tag)
    f.close()
    # f = open('test2.tsv', 'w', encoding='utf-8', newline='')
    # wr = csv.writer(f, delimiter='\t')
    # for tag in vocap:
    #         wr.writerow(str(tag))
    # f.close()
    #
    #
    with open("T[아].tsv", "w", encoding="utf-8") as g:
        for i in range(5):
            if i>0:
                g.write("\t")
            twrd="tag"+str(i)
            g.write(twrd)
        g.write("\n")
        for i in range(len(vocap)):
            wrd=vocap[i]
            if wrd == "":
                wrd="none"
            g.write(wrd)
            g.write("\t")
            g.write(wrd[0])
            g.write("\t")
            g.write(wrd[:3])
            g.write("\t")
            g.write(wrd[:3])
            g.write(" ")
            if wrd[:3] in ipc_ndic:
                g.write(ipc_ndic[wrd[:3]])
            else:
                g.write("UNK")
            g.write("\t")
            g.write(wrd)
            g.write(" ")
            if wrd in ipc_ndic:
                g.write(ipc_ndic[wrd])
            else:
                g.write("UNK")
            g.write("\n")
        # for tag in X:
        #     for i in range(299):
        #         g.write(str(tag[i]))
        #         g.write("\t")
        #     g.write(str(tag[299]))
        #     g.write("\n")
    return

def cut2(tex1):
    string=tex1
    string = re.sub("\]삭제", "\]", string)
    string = re.sub("\[청구항 [\d]{1,3}\]제[^서]{1,30}서", "", string)
    string = re.sub("\[청구항 [\d]+\]", "", string)
    string = re.sub("제[ ]{0,1}([\d]{1,3})[ ]{0,1}항[ 또에내지의중의]{1,4}", "", string)
    string = re.sub("제[\d]{1,2}", " ", string)
    string = re.sub("\([^\)\(]{1,40}\)","",string) #괄호 날림
    string = re.sub("길이", "사이즈", string)
    string = re.sub("([가-힣]+)장치[\n로는들를가에의와 .]", "\g<1>햄릿", string)
    string = re.sub("([가-힣]+) 장치[\n로는들를가에의와 .][^되된하한적]", " \g<1>햄릿", string)
    string = re.sub("([가-힣]+)[ ]{0,1}수단[\n으들은을이에의과 .]", "\g<1>햄릿", string)
    string = re.sub("([가-힣]+)[ ]{0,1}모듈[\n으은들을이에의과 .]", "\g<1>햄릿", string)
    string = re.sub("([가-힣]+)기구[\n로는를가들에의와 .]", "\g<1>햄릿", string)
    string = re.sub("([가-힣]+) 기구[\n로는를들가에의와 .][^되된하한적]", " \g<1>햄릿", string)
    string = re.sub("([가-힣]+)장비[\n로는를가에들의와 .]", "\g<1>햄릿", string)
    string = re.sub("([가-힣]+) 장비[\n로는를가에들의와 .][^되된하한적]", " \g<1>햄릿", string)
    string = re.sub("([가-힣]+)유닛[\n으은들을이에의과 .]", "\g<1>햄릿", string)
    string = re.sub("([가-힣]+) 유닛[\n으은들을이에의과 .][^되된하한적]", " \g<1>햄릿", string)
    string = re.sub("([가-힣]+)도구[\n로는를가에의들와 .]", "\g<1>햄릿", string)
    string = re.sub("([가-힣]+) 도구[\n로는를가에들의와 .][^되된하한적]", " \g<1>햄릿", string)
    string = re.sub("([가-힣]{2,})부[\n로는를가에의들와 .]", "\g<1>햄릿", string)
    string = re.sub("([가-힣]+) 부[\n로는를가에들의와 .][^되된하한적]", " \g<1>햄릿", string)
    string = re.sub("([가-힣]{2,})기[\n로는를가에의들와 .]", "\g<1>햄릿", string)
    string = re.sub("[^가-힣ㄱ-ㅎa-zA-Z0-9\-%^.<>=/ ]", " ", string)
    # string = re.sub("[^가-힣]상기", "", string)
    string = re.sub("적어도 하나의", "", string)
    string = re.sub("적어도 하나", "", string)
    string = re.sub("[복수여러다수\d]{1,3}[ ]{0,1}[개]{0,1}의", "", string)
    string = re.sub("[복수여러\d]{1,3}[ ]{0,1}개", "", string)
    string = re.sub("[ ]{2,}", " ", string)
    string = re.sub(" [에와과을를이가로] ", " ", string)
    return string

def cut(tex1):
    string=tex1
    string = re.sub("\[청구항 [\d]{1,3}\]제[^서]{1,30}서", "", string)
    string = re.sub("\[청구항 [\d]+\]", "", string)
    string = re.sub("제[ ]{0,1}([\d]{1,3})[ ]{0,1}항[ 또에내지의중의]{1,4}", "", string)
    string = re.sub("제[\d]{1,2}", " ", string)
    string = re.sub("[^가-힣ㄱ-ㅎa-zA-Z0-9\+\-*%^.<>/ ]", " ", string)
    # string = re.sub("[^가-힣]상기", "", string)
    string = re.sub("적어도 하나의", "", string)
    string = re.sub("적어도 하나", "", string)
    string = re.sub("[복수여러다수\d]{1,3}[ ]{0,1}[개]{0,1}의", "", string)
    string = re.sub("[복수여러\d]{1,3}[ ]{0,1}개", "", string)
    string = re.sub("[ ]{2,}", " ", string)
    string = re.sub(" [에와과을를이가로] ", " ", string)
    return string

def trans2(claim):
    buf=[]
    buf1=[]
    string = claim
    # string = re.sub("\([^\(]+", "", string)
    string = cut2(string)
    string = re.sub("[^가-힣]상기", "", string)
    txt1 = m.parse(string)
    txt = txt1.split("\n")
    for word in txt:
        if len(word) > 5:
            pos = word.split("\t")[1]
            name = word.split("\t")[0]
            name= re.sub("(?<=[가-힣])[\d][^\n]+", "", name)
            if pos.startswith('N') or pos.startswith('SL'):
                if name in dic and name!="장치":
                    buf.append(name)
    for wrd in buf:
        buf1.append(str(dic.index(wrd)))
    return buf1

def lod2():
    workbook = xlrd.open_workbook('C:/Users/User/PycharmProjects/patent\\testset3.xls')
    worksheet = workbook.sheet_by_index(0)
    nrows = worksheet.nrows
    clst=[]
    ipst = []
    ipst2 = []
    ipst3 = []
    for row_num in range(nrows):
        clst.append(worksheet.cell_value(row_num, 3))
    blst=[]
    c=0
    for doc in clst:
        print(c)
        c=c+1
        blst.append(trans2(doc))
    return blst

def lod():
    workbook = xlrd.open_workbook('C:/Users/User/PycharmProjects/patent\\testset.xls')
    worksheet = workbook.sheet_by_index(0)
    nrows = worksheet.nrows
    clst=[]
    ipst = []
    ipst2 = []
    ipst3 = []
    ipst4 = []
    for row_num in range(8, nrows):
        ipst1 = []
        tdic=dict()
        tdic2=dict()
        tdic3 = dict()
        clst.append(worksheet.cell_value(row_num, 4))
        buf=worksheet.cell_value(row_num, 3)
        buf2=re.sub("\([\d.]+\)","",buf) #G06F 40/20(2020.01)|G06N 3/08(2006.01)
        buf4=re.sub(" ", "",buf2)
        buf7=buf4.split("|")
        ipst4.append(buf7)
        buf4=re.sub("\/[^|]+","",buf4)
        buf5=buf4.split("|")
        for itm3 in buf5:
            if itm3 in tdic3:
                tdic3[itm3]=tdic3[itm3]+1
            else:
                tdic3[itm3]=1
        buf6 = list(tdic3.keys())
        ipst3.append(buf6)
        buf3=buf2.split("|")
        for itm in buf3:
            ipst1.append(itm[:4])
        for itm1 in ipst1:
            if itm1 in tdic:
                tdic[itm1]=tdic[itm1]+1
            else:
                tdic[itm1]=1
        buf=list(tdic.keys())
        ipst.append(buf)
        for itm2 in buf:
            if itm2[:3] in tdic:
                tdic2[itm2[:3]]=tdic2[itm2[:3]]+1
            else:
                tdic2[itm2[:3]]=1
        buf2 = list(tdic2.keys())
        ipst2.append(buf2)
    # blst=[]
    # c=0
    # for doc in clst:
    #     print(c)
    #     c=c+1
    #     blst.append(trans2(doc))
    return ipst,ipst2, ipst3, ipst4

def lodC():
    workbook = xlrd.open_workbook('C:/Users/User/PycharmProjects/patent\\testset3.xls')
    worksheet = workbook.sheet_by_index(0)
    nrows = worksheet.nrows
    clst=[]
    ipst = []
    ipst2 = []
    ipst3 = []
    ipst4 = []
    for row_num in range(nrows):
        ipst1 = []
        tdic=dict()
        tdic2=dict()
        tdic3 = dict()
        # clst.append(worksheet.cell_value(row_num, 4))
        buf=worksheet.cell_value(row_num, 4)
        buf2=re.sub("\([\d.]+\)","",buf) #G06F 40/20(2020.01)|G06N 3/08(2006.01)
        buf4=re.sub(" ", "",buf2)
        buf7=buf4.split("|")
        ipst4.append(buf7)
        buf4=re.sub("\/[^|]+","",buf4)
        buf5=buf4.split("|")
        for itm3 in buf5:
            if itm3 in tdic3:
                tdic3[itm3]=tdic3[itm3]+1
            else:
                tdic3[itm3]=1
        buf6 = list(tdic3.keys())
        ipst3.append(buf6)
        buf3=buf2.split("|")
        for itm in buf3:
            ipst1.append(itm[:4])
        for itm1 in ipst1:
            if itm1 in tdic:
                tdic[itm1]=tdic[itm1]+1
            else:
                tdic[itm1]=1
        buf=list(tdic.keys())
        ipst.append(buf)
        for itm2 in buf:
            if itm2[:3] in tdic:
                tdic2[itm2[:3]]=tdic2[itm2[:3]]+1
            else:
                tdic2[itm2[:3]]=1
        buf2 = list(tdic2.keys())
        ipst2.append(buf2)
    # blst=[]
    # c=0
    # for doc in clst:
    #     print(c)
    #     c=c+1
    #     blst.append(trans2(doc))
    return ipst,ipst2, ipst3, ipst4

def test():
    tlist=[]
    model = gensim.models.doc2vec.Doc2Vec.load("doc2vec[아].model")
    for i in range(len(blst)):
        print(i, end='')
        a=model.docvecs.most_similar([model.infer_vector(blst[i])], topn=10)
        hit_flag=False
        for lst in a:
            if lst[0][:3] in ipst2[i] :
                print("  HIT  ", end='')
                print(lst[1])
                hit_flag = True
                break
        if hit_flag==False:
            print("  Fail")
        tlist.append(hit_flag)
    return tlist

def test2():
    tlist=[]
    model = gensim.models.doc2vec.Doc2Vec.load("doc2vec[하].model")
    for i in range(len(blst)):
        print(i, end='')
        a=model.docvecs.most_similar([model.infer_vector(blst[i])], topn=1000)
        tdic=dict()
        for lst1 in a:
            # temp=re.sub("\/[\s\S]+", "", lst1[0])
            # tdic[temp] = 0
            # if len(lst1[0]) == 4:
            # if "/" not in lst1:
            tdic[lst1[0][:4]]=0

            # tdic[lst1[0][:4]]=0
            if len(tdic) == 10:
                break
        # if len(tdic) <10:
        #     print("못채움")
        b=list(tdic.keys())
        hit_flag=False
        for lst in b:
            if lst in ipst[i] :
                print("  HIT")
                hit_flag = True
                break
        if hit_flag==False:
            print("  Fail")
        tlist.append(hit_flag)
    counter = collections.Counter(tlist)
    return counter

def test3():
    tlist=[]
    model = gensim.models.doc2vec.Doc2Vec.load("doc2vec[바].model")
    for i in range(len(blst)):
        print(i, end='')
        a=model.docvecs.most_similar([model.infer_vector(blst[i])], topn=5000)
        hit_flag=False
        for lst in a:
            if lst[0] in ipst[i] :
                print("  HIT   ", end='')
                print(lst[1])
                hit_flag = True
                break
        if hit_flag==False:
            print("  Fail")
        tlist.append(hit_flag)
    return tlist

def test4(bset, tset1):
    rst=[]
    c=0
    for doc in tset1:
        print(c)
        c=c+1
        for doc2 in bset:
            rst.append(cos(doc,doc2))
    AVG=sum(rst, 0.0)/len(rst)
    return AVG

def test5():
    tlist=[]
    model = gensim.models.doc2vec.Doc2Vec.load("doc2vec[차].model")
    for i in range(len(blst)):
        print(i, end='')
        a=model.docvecs.most_similar([model.infer_vector(blst[i])], topn=500)
        tdic=dict()
        for lst1 in a:
            # if len(lst1[0])>4 and "/" not in lst1[0]:
            #     tdic[lst1[0]]=0
            # if "/" in lst1[0]:
            #     butx=re.sub("\/[\s\S]+","",lst1[0])
            #     tdic[butx]=0
            # else:
            #     tdic[lst1[0]]=0
            if "/" in lst1[0] or len(lst1[0])>4:
                butx = re.sub("\/[\s\S]+", "", lst1[0])
                tdic[butx] = 0
            if len(tdic) == 10:
                break
        if len(tdic) <10:
            print("못채움")
        b=list(tdic.keys())
        hit_flag=False
        for lst in b:
            if lst in ipst3[i] :
                print("  HIT")
                hit_flag = True
                break
        if hit_flag==False:
            print("  Fail")
        tlist.append(hit_flag)
    counter = collections.Counter(tlist)
    return counter

def test6():
    tlist=[]
    model = gensim.models.doc2vec.Doc2Vec.load("doc2vec[아].model")
    for i in range(len(blst)):
        print(i, end='')
        a=model.docvecs.most_similar([model.infer_vector(blst[i])], topn=50)
        tdic = dict()
        for lst1 in a:
            if "/" in lst1[0]:
                tdic[lst1[0]]=0
            if len(tdic) == 10:
                break
        b = list(tdic.keys())
        hit_flag = False
        for lst2 in b:
            if lst2 in ipst4[i]:
                print("  HIT")
                hit_flag = True
                break
        if hit_flag == False:
            print("  Fail")
        tlist.append(hit_flag)
    counter = collections.Counter(tlist)
    return counter

def fu(CN):
    n="2020"
    temp=dict()
    c=0
    for lst in CN:
        if c%1000==0:
            print(c)
        c=c+1
        if lst[1] != n:
            pick = "[" + str(n) + "].pickle"
            with gzip.open(pick, 'wb') as f:
                pickle.dump(temp, f, pickle.HIGHEST_PROTOCOL)
            n=lst[1]
            temp=dict()
            temp[lst[0]]=lst[2]
        else:
            temp[lst[0]]=lst[2]
    pick = "[" + str(n) + "].pickle"
    with gzip.open(pick, 'wb') as f:
        pickle.dump(temp, f, pickle.HIGHEST_PROTOCOL)
    return

def fu2(CN):
    temp=[]
    c=0
    for wrd in CN:
        if c%1000==0:
            print(c)
        c=c+1
        nd=int(wrd[2:6])-1978
        if nd<0 or nd>42:
            print(nd+1978)
            temp.append([wrd, 9999999])
            continue
        CD=ND[nd]
        if wrd in CD:
            temp.append([wrd,CD[wrd]])
        else:
            temp.append([wrd, 9999999])
    return temp

def fu3(temp):
    fq=[]
    c = 0
    for lst in temp:
        if c%1000==0:
            print(c)
        c=c+1
        bufd = dict()
        if lst[1]==9999999:
            fq.append([""])
        else:
            string=DB[lst[1]][6].replace(" ","")
            string.upper()
            cpt=re.sub("\([^|]+", "", string)
            string1 = cpt.split("|")
            for wrd in string1:
                if wrd in bufd:
                    bufd[wrd] = bufd[wrd] + 1
                else:
                    bufd[wrd] = 1
            buf=list(bufd.keys())
            fq.append(buf)
    return fq

def cos(x, y):
    return np.dot(x, y) / (np.sqrt(np.dot(x, x)) * np.sqrt(np.dot(y, y)))

def sample(idx):
    a1 = int((idx) / 5000)
    b1 = int((idx) % 5000)
    workbook = xlrd.open_workbook(f_list[a1])
    worksheet = workbook.sheet_by_index(0)
    string1 =re.sub("\([\s\S]*", "", worksheet.cell_value((8 + b1), 5))
    string2 =re.sub("\n", "", worksheet.cell_value((8 + b1), 6))
    string3 =re.sub("\([\d.]+\)", "", worksheet.cell_value((8 + b1), 7))
    # print(worksheet.cell_value((8 + b1), 5))
    print(string1)
    print(string2)
    print(string3)
    return

from itertools import takewhile

is_tab = '\t'.__eq__

def build_tree(lines):
    lines = iter(lines)
    stack = []
    IPTREE=[]
    for line in lines:
        buf=[]
        indent = len(list(takewhile(is_tab, line)))
        stack[indent:] = [line.lstrip()]
        for wrd in stack:
            buf.append(wrd)
        IPTREE.append(buf)
        print(stack)
    return IPTREE


f1 = gzip.open("사전(정리).pickle", 'rb')
dic = pickle.load(f1)
f1.close()
f1 = gzip.open("NTESTSET[C1].pickle", 'rb')
blst = pickle.load(f1)
f1.close()
f1 = gzip.open("출원번호.pickle", 'rb')
CN = pickle.load(f1)
f1.close()
# f1 = gzip.open("IPCTREE.pickle", 'rb')
# IPTREE = pickle.load(f1)
# f1.close()
# f1 = gzip.open("IP사전.pickle", 'rb')
# ipc_ndic = pickle.load(f1)
# f1.close()

# f1 = gzip.open("DBDBDB.pickle", 'rb')
# DB = pickle.load(f1)
# f1.close()

ipst, ipst2, ipst3, ipst4=lodC()
model = gensim.models.doc2vec.Doc2Vec.load("doc2vec[타].model")
#
ND=[]
for i in range(1978,2021):
    pick = "[" + str(i) + "].pickle"
    f1 = gzip.open(pick, 'rb')
    ND.append(pickle.load(f1))
    f1.close()


c=0
for wrd in CN2:
    CN3.append([wrd.replace("-",""),wrd[3:7],c])
    c=c+1

for lst in IPLT:
    for wrd in lst:
        if wrd in DIC:
            DIC[wrd]=DIC[wrd]+1
        else:
            DIC[wrd]=0

counter = collections.Counter(DIC)
counter1 = counter.most_common()


f2 = open("IPC2.txt", "r", encoding="utf-8")
ipt=f2.readlines()

ipt2=[]

for wrd in ipt:
    ipt2.append(wrd.replace("\n",""))

IPCTREE=build_tree(ipt2)

buf=[]
buf1=[]

for lst in IPCTREE:
    buf1=[]
    for wrd in lst:
        wrd=wrd.replace("\t","")
        buf1.append(wrd)
    buf.append(buf1)

ipdex=[wrd[-1] for wrd in buf]

ipdic=dict()

for i in range(len(ipdex)):
    ipdic[ipdex[i]]=buf[i]

with gzip.open('IPC사전.pickle', 'wb') as f:
    pickle.dump(ipdic, f, pickle.HIGHEST_PROTOCOL)


ddic=dict()
c=0
for list1 in IPlst:
    if c%1000 ==0
        print(c)
    c=c+1
    for wrd in list1:
        if wrd in ddic:
            ddic[wrd]=ddic[wrd]+1
        else:
            ddic[wrd]=0


teset1=blst[:1000]
teset2=blst[1000:]
bset=[]
c=0
for doc in teset1:
    print(c)
    c=c+1
    bset.append(model.infer_vector(doc))
tset1=[]
c=0
for doc in teset2:
    print(c)
    c=c+1
    tset1.append(model.infer_vector(doc))
test4(bset, tset1)
#
#
# with gzip.open("testset2.pickle", 'wb') as f:
#     pickle.dump(blst2, f, pickle.HIGHEST_PROTOCOL)
#
# tclaim="[청구항 1]수술 로봇 시스템으로서,적어도 하나의 선형 변위가능 구동 부재를 포함하는 액추에이터;상기 적어도 하나의 구동 부재에 의해 작동되는 적어도 하나의 자유도를 갖는 수술 기구;상기 액추에이터와 상기 수술 기구 사이에 개재되는 멸균 어댑터 - 상기 멸균 어댑터는 가요성 장벽 및 상기 가요성 장벽과 일체로 형성된 복수의 연장가능 커버를 포함하고, 상기 복수의 연장가능 커버는 상기 복수의 구동 부재를 수용하도록 배열됨 -; 및상기 멸균 어댑터를 가로질러 상기 액추에이터와 상기 수술 기구를 결합시키는 상호잠김 배열체(interlocked arrangement) - 상기 상호잠김 배열체는 상기 액추에이터가 상기 수술 기구의 적어도 하나의 자유도를 작동시킬 때 상기 액추에이터 및 상기 수술 기구를 함께 가압함 - 를 포함하는, 시스템. [청구항 2]제1항에 있어서, 상기 액추에이터는 기구 장착 인터페이스를 포함하고, 가요성 장벽은 상기 기구 장착 인터페이스에 순응하는, 시스템. [청구항 3]제2항에 있어서, 상기 기구 장착 인터페이스는 공동을 포함하고, 상기 가요성 장벽은 상기 공동에 순응하고; 상기 공동은 상기 수술 기구가 상기 액추에이터와 상기 멸균 어댑터의 결합해제를 실질적으로 방지하도록 상기 수술 기구의 일부분을 수용하도록 구성되는, 시스템. [청구항 4]제1항에 있어서, 상기 멸균 어댑터는 상기 가요성 장벽에 결합된 프레임을 포함하고, 상기 가요성 장벽은 상기 프레임과 함께 공사출 성형되는, 시스템. [청구항 5]제1항에 있어서, 적어도 하나의 연장가능 커버는 상기 적어도 하나의 연장가능 커버 내에 수용된 구동 부재의 선형 변위에 따라 휴지 상태와 완전 연장 상태 사이에서 전이되는, 시스템. [청구항 6]제1항에 있어서, 적어도 하나의 연장가능 커버는 탄성중합체 재료를 포함하는, 시스템. [청구항 7]제1항에 있어서, 적어도 하나의 연장가능 커버는 폐쇄된 원위 단부를 포함하고, 상기 원위 단부는 보강된, 시스템. [청구항 8]제7항에 있어서, 상기 원위 단부는 상기 적어도 하나의 연장가능 커버의 벽보다 두꺼운, 시스템. [청구항 9]제7항에 있어서, 상기 원위 단부는 상기 적어도 하나의 연장가능 커버의 벽보다 단단한 재료를 포함하는, 시스템. [청구항 10]제1항에 있어서, 상기 멸균 어댑터에 결합되는 멸균 드레이프(drape)를 추가로 포함하는, 시스템. [청구항 11]제1항에 있어서, 상기 상호잠김 배열체는 상기 액추에이터에 결합된 제1 부분 및 상기 수술 기구에 결합된 제2 부분을 포함하는, 시스템. [청구항 12]제11항에 있어서, 상기 제1 부분은 제1 상호잠금 부재를 포함하고, 상기 제2 부분은 상기 제1 상호잠금 부재와 맞물리도록 구성된 제2 상호잠금 부재를 포함하는, 시스템. [청구항 13]제11항에 있어서, 상기 상호잠김 배열체의 제2 부분은 래치(latch)를 포함하는, 시스템. [청구항 14]제13항에 있어서, 상기 수술 기구는 상기 액추에이터와 상기 수술 기구를 해제가능하게 결합시키기 위해 상기 래치에 작동식으로 결합되는 손잡이를 포함하는, 시스템. [청구항 15]제14항에 있어서, 상기 래치는 선회가능하고, 상기 손잡이는 상기 래치의 받침대(fulcrum)에 작동식으로 결합되는, 시스템. [청구항 16]제1항에 있어서, 상기 상호잠김 배열체는, 상기 액추에이터가 상기 수술 기구의 적어도 하나의 자유도를 작동시키고 반작용력(reaction force)을 야기할 때, 상기 상호잠김 배열체가 상기 반작용력을 압축력으로 레버리지(leverage)하도록 구성되는, 시스템. [청구항 17]수술 로봇 시스템에서 멸균을 위한 방법으로서,적어도 하나의 선형 변위가능 구동 부재를 포함하는 액추에이터에 멸균 어댑터를 결합시키는 단계;상호잠김 배열체를 통해 상기 멸균 어댑터를 가로질러 상기 액추에이터에 수술 기구를 결합시켜서, 상기 멸균 어댑터가 상기 액추에이터와 상기 수술 기구 사이에 개재되게 하는 단계; 및상기 수술 기구의 적어도 하나의 자유도를 작동시키도록 상기 구동 부재를 제어하는 단계 - 상기 상호잠김 배열체는 상기 구동 부재가 상기 수술 기구의 적어도 하나의 자유도를 작동시킬 때 상기 액추에이터 및 상기 수술 기구를 함께 가압함 - 를 포함하는, 방법. [청구항 18]제17항에 있어서, 적어도 부분적으로 상기 상호잠김 배열체를 맞물림해제함으로써 상기 수술 기구를 상기 액추에이터로부터 결합해제하는 단계를 추가로 포함하는, 방법. [청구항 19]제18항에 있어서, 상기 수술 기구를 상기 액추에이터로부터 결합해제하는 단계는 상기 수술 기구에 결합된 손잡이를 상기 액추에이터 및 멸균 어댑터로부터 멀어지게 조작하여, 그에 의해 상기 상호잠김 배열체의 제1 부분과 제2 부분을 분리하는 단계를 포함하고, 상기 제1 부분은 상기 액추에이터에 결합되고 상기 제2 부분은 상기 수술 기구에 결합되는, 방법. [청구항 20]제19항에 있어서, 상기 상호잠김 배열체를 맞물림해제하는 단계는 상기 손잡이를 상기 액추에이터 및 멸균 어댑터로부터 멀어지게 당기는 단계를 포함하는, 방법."
