

r"""
Doc2Vec Model
=============

Introduces Gensim's Doc2Vec model and demonstrates its use on the Lee Corpus.

"""
IPlist = ["H01", "H04", "G06", "A61", "B60", "G01", "F16", "A47", "G02", "B65", "H02", "C07", "H05", "G11", "C08",
          "B01", "A01", "G09", "A23", "F24", "C09", "E04", "G03", "B29", "C12", "B62", "H03", "B23", "F21", "A63",
          "F25", "F02", "E02", "G08", "D06", "C02", "A45", "B32", "E05", "C23", "E01", "B63", "F01", "F04", "B21",
          "G05", "B05", "C01", "B41", "B25", "E03", "C04", "C22", "B66", "G07", "F23", "E06", "A41", "G10", "B22",
          "C21", "B24", "C10", "A43", "C03", "B82", "F28", "B08", "A44", "B26", "F03", "D01", "A62", "B42", "C25",
          "G16", "B09", "B43", "D04", "F27", "C11", "B02", "B28", "F17", "F26", "E21", "A46", "G21", "B61", "B44",
          "D21", "B64", "D03", "A24", "F41", "B30", "B67", "D02", "F15", "G04", "C05", "A21", "A42", "B07", "B27",
          "C30", "B03", "D05", "F42", "F22", "B31", "B04", "B33", "A22", "B81", "B06", "D07", "B68", "C14", "C06",
          "G12", "C40", "C13", "G99", "F99"]

ipclist = []
with open("IPlist.txt", "r", encoding="utf-8") as fp:
    for string in fp:
        ipclist.append(string[:-1].split(" "))

pclist = []
for doc in ipclist:
    if len(doc) > 1:
        buf = []
        for wrd in doc:
            if wrd in IPlist:
                buf.append(IPlist.index(wrd))
        if buf == []:
            pclist.append("NONE")
        else:
            pclist.append(IPlist[min(buf)])
    else:
        pclist.append(doc[0])
        
import pickle
import gzip
f1 = gzip.open("CPC[카].pickle", 'rb')
cplist = pickle.load(f1)
f1.close()

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)



import os
import gensim
# Set file names for train and test data
test_data_dir = os.path.join(gensim.__path__[0], 'test', 'test_data')
lee_train_file = os.path.join(test_data_dir, 'lee_background.cor')
lee_test_file = os.path.join(test_data_dir, 'lee.cor')

###############################################################################
# Define a Function to Read and Preprocess Text
# ---------------------------------------------
#
# Below, we define a function to:
#
# - open the train/test file (with latin encoding)
# - read the file line-by-line
# - pre-process each line (tokenize text into individual words, remove punctuation, set to lowercase, etc)
#
# The file we're reading is a **corpus**.
# Each line of the file is a **document**.
#
# .. Important::
#   To train the model, we'll need to associate a tag/number with each document
#   of the training corpus. In our case, the tag is simply the zero-based line
#   number.


import smart_open

def read_corpus(fname, tokens_only=False):
    with smart_open.open(fname, encoding="UTF-8") as f:
        for i, line in enumerate(f):
            # print(line)
            tokens = gensim.utils.simple_preprocess(line)
            # print(tokens)
            if tokens_only:
                yield tokens
            else:
                # For training data, add tags
                yield gensim.models.doc2vec.TaggedDocument(tokens, cplist[i])

train_corpus = list(read_corpus(lee_train_file))
test_corpus = list(read_corpus(lee_test_file, tokens_only=True))

###############################################################################
# Let's take a look at the training corpus
#
print(train_corpus[:2])

###############################################################################
# And the testing corpus looks like this:
#
print(test_corpus[:2])

###############################################################################
# Notice that the testing corpus is just a list of lists and does not contain
# any tags.
#

###############################################################################
# Training the Model

model = gensim.models.doc2vec.Doc2Vec(vector_size=300, min_count=2, epochs=40, workers=14)
# model = gensim.models.doc2vec.Doc2Vec.load("doc2vec[나].model")

###############################################################################
# Build a vocabulary
model.build_vocab(train_corpus)

###############################################################################
# Essentially, the vocabulary is a dictionary (accessible via
# ``model.wv.vocab``\ ) of all of the unique words extracted from the training
# corpus along with the count (e.g., ``model.wv.vocab['penalty'].count`` for
# counts for the word ``penalty``\ ).
#

###############################################################################
# Next, train the model on the corpus.
# If the BLAS library is being used, this should take no more than 3 seconds.
# If the BLAS library is not being used, this should take no more than 2
# minutes, so use BLAS if you value your time.
#


f21=open("epochTEST.txt", 'w', encoding="utf-8")

import collections


f1 = gzip.open("NTESTSET[C1].pickle", 'rb')
blst = pickle.load(f1)
f1.close()

import re
import xlrd

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
        buf=worksheet.cell_value(row_num, 2)
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

ipst, ipst2, ipst3, ipst4=lodC()

def test():
    tlist1= []
    tlist2 = []
    tlist3 = []
    for i in range(len(blst)):
        a=model.docvecs.most_similar([model.infer_vector(blst[i])], topn=1000)
        tdic1 = dict()
        tdic2 = dict()
        tdic3 = dict()
        for lst1 in a:
            if len(tdic1) < 10:
                tdic1[lst1[0][:3]] = 0
            if len(tdic2) < 10:
                tdic2[lst1[0][:4]] = 0
            if len(tdic3) < 10:
                temp = re.sub("\/[\s\S]+", "", lst1[0])
                tdic3[temp] = 0
            if len(tdic1) == 10 and len(tdic2) == 10 and len(tdic3) == 10:
                break
        b1= list(tdic1.keys())
        b2 = list(tdic2.keys())
        b3 = list(tdic3.keys())
        hit_flag=False
        for wrd in b1:
            if wrd in ipst2[i] :
                hit_flag = True
                break
        tlist1.append(hit_flag)
        hit_flag = False
        for wrd in b2:
            if wrd in ipst[i] :
                hit_flag = True
                break
        tlist2.append(hit_flag)
        hit_flag = False
        for wrd in b3:
            if wrd in ipst3[i] :
                hit_flag = True
                break
        tlist3.append(hit_flag)
    counter1 = collections.Counter(tlist1)
    counter2 = collections.Counter(tlist2)
    counter3 = collections.Counter(tlist3)
    ct1=counter1[True]
    ct2=counter2[True]
    ct3=counter3[True]
    return ct1, ct2, ct3
fs=[]
for num in range(5):
    model.train(train_corpus, total_examples=model.corpus_count, epochs=2)
    ep=str((num+1)*2)
    pi = "Test[" + ep + "].model"
    model.save(pi)
    model = gensim.models.doc2vec.Doc2Vec.load(pi)
    r1, r2, r3= test()
    pick = "Test[" + ep + "].txt"
    with open(pick, 'w', encoding="utf-8") as g1:
        g1.write(ep)
        g1.write("\t")
        g1.write(str(r1))
        g1.write("\t")
        g1.write(str(r2))
        g1.write("\t")
        g1.write(str(r3))
        g1.write("\n")

model.train(train_corpus, total_examples=model.corpus_count, epochs=model.epochs)



model=gensim.models.doc2vec.Doc2Vec.load(pi)


model.save("doc2vec[하].model")

###############################################################################
# Now, we can use the trained model to infer a vector for any piece of text
# by passing a list of words to the ``model.infer_vector`` function. This
# vector can then be compared with other vectors via cosine similarity.
# #
# vector = model.infer_vector(["1" ,"2" ,"3" ,"4" ,"5" ,"6" ,"7" ,"8" ,"9" ,"10" ,"11"])
# print(vector)


##############################################################################



f1 = gzip.open("NTESTSET[C1].pickle", 'rb')
blst = pickle.load(f1)
f1.close()
import csv
import re
import xlrd
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
ipst, ipst2, ipst3, ipst4=lodC()


