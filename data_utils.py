import re
import xlrd
from konlpy.tag import Komoran
from multiprocessing import Process, Queue
komoran = Komoran()
# from konlpy.tag import Kkma
# kkma=Kkma()
# import time
import glob
import collections
import time
import sys
import pickle
import math
# import gzip
import MeCab
from konlpy.tag import Komoran
import pickle
import math
import numpy as np
from numpy.linalg import norm
from operator import itemgetter
import MeCab
import gzip
import gensim

f1 = gzip.open("IPIP.pickle", 'rb')
idic = pickle.load(f1)
f1.close()
dst = list(idic.keys())
# komoran = Komoran()
# m = MeCab.Tagger()

start_time = time.time()

def sims(n,tk,model):
    pick = "INF[" + str(n) + "].pickle"
    inv=[]
    c=0
    for doc in tk:
        if c%100==0:
            print("%d\t\t%d"%(n,c))
        c=c+1
        doc2=[]
        for num in doc:
            doc2.append(str(num))
        inv.append(model.infer_vector(doc2))
    with gzip.open(pick, 'wb') as f:
        pickle.dump(inv, f, pickle.HIGHEST_PROTOCOL)
    return

def snoun(word3):

    pdic=[]
    k=len(word3)
    buf33 = ddic.keys()

    word3 = []
    for word2 in buf33:

        word4=re.sub("제[\d]{1,2}", "", word2)
        word4=re.sub("[^가-힣 ]","",word4)

    word3.sort(key=len, reverse=False)

    print(word3)
    for i in range(len(word3) - 1):
        print(i)
        time1 = (k - i) / ((i+1) / (time.time() - start_time))
        sys.stdout.write("\r처리건수: %d건\t사전길이:%d개\t남은시간: %.2f분\t진행율:%.2f%%" % (
        i, len(pdic), (time1 / 60), (100*i / k)))

        ln = len(word3[i])
        if ln == 1:
            continue
        for word4 in word3[i + 1:]:
            if word3[i] == word4[:ln] and len(word4[ln:]) != 1:
                pdic.append(word4[ln:])
                pdic.append(word3[i])
                # if word4[ln:] in pdic:
                #     pdic[word4[ln:]] = pdic[word4[ln:]] + 1
                # else:
                #     pdic[word4[ln:]] = 1
            # if word3[i] == word4[-ln:] and len(word4[:-ln]) !=1:
            #     if word4[:-ln] in pdic:
            #         pdic[word4[:-ln]] = pdic[word4[:-ln]] + 1
            #     else:
            #         pdic[word4[:-ln]] = 1
            # if word3[i] in pdic:
            #     pdic[word3[i]]=pdic[word3[i]]+1
            # else:
            #     pdic[word3[i]]=1
    # ddic.update(pdic)
    return pdic

def snoun1(word3, word5):
    word2=[]
    for i in range(len(word3)):
        for k in range(len(word5)):
            if word3[i] == word5[k][2:]:
                word2.append(word5[k][:2])
        print(i)
    return word2

def nor(tfidf1):
    temp=[]
    count=0
    for doc in tfidf1:
        if doc == []:
            temp.append([])
            print(count)
            count=count+1
            continue
        t=np.asarray(doc, dtype=np.float16)
        t = np.transpose(t)
        idx = t[0]
        idx = np.array(idx, dtype=np.int32)
        vec = t[1]
        len_vec = norm(vec)
        vec = vec / len_vec
        temp.append([idx,vec])
        print(count)
        count=count+1
    return temp

def norm1(tfidf1):
    temp = []
    count = 0
    for doc in tfidf1:
        if doc == []:
            temp.append([])
            print(count)
            count=count+1
            continue
        idx=[]
        val=[]
        buf=0
        ln=len(doc)
        for pair in doc:
            buf=buf+(pair[1]*pair[1])
        buf1=round(math.sqrt(buf),4)
        for pair in doc:
            idx.append(pair[0])
            rst=round(pair[1]/buf1, 4)
            val.append(rst)
        temp.append([idx,val])
        print(count)
        count = count + 1
    return temp

def said(txt):
    trash = []
    exlist1 = ["부", "홈", "암", "홀"]
    exlist2 = ["로봇", "이면", "이외", "장비", "모터", "링크", "챔버", "전극", "배관", "밸브", "장치", "단부", "바디", "모듈", "부재", "라인", "홀더",
               "탱크", "구멍", "단계", "본체", "정보", "표면", "헤드", "렌즈"]
    exlist3 = ["조인트", "프리즘", "본체부", "공급관", "삽입홀", "브라켓", "수용부", "하우징", "결합부", "장착부", "지지체", "어레이", "고정부", "회전축", "패스너",
               "시스템", "연결부", "이미지", "연장부"]
    txt0 = m.parse(txt)
    txt2 = re.findall("([\S]{1,10})	([A-IJK-Z+]{1,}),", txt0)
    # txt2= re.findall("([\S]{1,10})	([A-Z+]{1,}),",txt0)

    wlist = []
    txt3 = ""
    for pair in txt2:
        wlist.append([pair[0], pair[1]])
        txt3 = txt3 + " / " + pair[0] + "(" + pair[1] + ")"
    # print(txt3)  # 디버그0 포인트
    txt3 = re.sub(r" \(\(SSO\) \/ [\S]{1,10}\(S[A-Z]{1,2}\) \/ \)\(SSC\) \/", "", txt3)

    txt3 = txt3.replace("G) / 복수(NNG) / 개(NNBC) / 의(JKG) / ", "G) / ")
    txt3 = txt3.replace("G) / 복수(NNG) / 의(JKG) / ", "G) / ")
    txt3 = txt3.replace("G) / 여러(MM) / 개(NNBC) / 의(JKG) / ", "G) / ")
    txt3 = txt3.replace("G) / 다(MAG) / 수개(NNG) / 의(JKG) / ", "G) / ")
    txt3 = txt3.replace("G) / 다수(NNG) / 의(JKG) / ", "G) / ")
    txt3 = txt3.replace("G) / 한(MM) / 쌍(NNG) / 의(JKG) / ", "G) / ")
    txt3 = txt3.replace("상기(NNG) / 각각(NNG) / 의(JKG) / ", "상기(NNG) / ")
    txt3 = txt3.replace("상기(MAG) / 각각(NNG) / 의(JKG) / ", "상기(MAG) / ")
    txt3 = txt3.replace("G) / 2(SN) / 개(NNBC) / 의(JKG) / ", "G) / ")
    txt3 = txt3.replace("G) / 3(SN) / 개(NNBC) / 의(JKG) / ", "G) / ")
    txt3 = txt3.replace("G) / 적어도(MAG) / 하나(NR) / 의(JKG) / ", "G) / ")
    txt3 = txt3.replace("G) / 적어도(MAG) / 하나(NR) / 이상(NNG) / 의(JKG) / ", "G) / ")

    txt3 = txt3.replace("이후(NNG)", "이후(JX)")
    # txt3 = txt3.replace("내(NP+JKG)", "내(NP)")
    txt3 = txt3.replace("(NNG) / 부가(NNG) /", "부(NNG) / 가(JKS) /")
    txt3 = txt3.replace("(NNG) / 체가(NNG) /", "체(NNG) / 가(JKS) /")
    txt3 = txt3.replace("/ 이(VCP) / 면(EC) /", "/ 이면(JEC) /")
    txt3 = txt3.replace("/ 망은(NNG) /", "/ 망(NNG) / 은(JX) /")
    txt3 = txt3.replace("(NNB+JKO)", "(NNB)")
    txt3 = txt3.replace("/ 부를(VV+ETM) /", "/ 부(NNG) / 를(JKO) /")
    txt3 = txt3.replace("/ 회(NNBC) / 전(NP+JX) /", "/ 회전(NNG) /")
    txt3 = re.sub(r"상기\(", "\n상기(", txt3)
    # print(txt3) #디버그포인트
    txt3 = re.sub(
        "상기\([A-Z]{1,5}\) \/( 제\([A-Z]{1,5}\) \/ [\d]\(SN\) \/) [및내지또는]{1,2}\([A-Z]{1,5}\) \/( 제\(MM\) \/ [\d]\(SN\) \/)([^\n]*)",
        "상기(NNG) /\g<1>\g<3>\n상기(NNG) /\g<2>\g<3>", txt3)

    txt3 = re.sub(
        "상기\([A-Z]{1,5}\) \/( 제\([A-Z]{1,5}\) \/ [\d]\(SN\) \/) [및내지또는]{1,2}\([A-Z]{1,5}\) \/( [\d]\(SN\) \/)([^\n]*)",
        "상기(NNG) /\g<1>\g<3>\n상기(NNG) / 제(XPN) /\g<2>\g<3>", txt3)

    txt3 = re.sub("\(([A-Z]{1})[^)]*\+[^)]*\)", "(\g<1>\g<1>)", txt3)  # (VV+AS)
    # print(txt3) #디버그 포인트
    txt41 = re.findall("상기\([NM][A-Z][A-Z]{0,2}\) [^J\n]*\(", txt3)
    txt42 = re.findall("상기\([NM][A-Z][A-Z]{0,2}\) \/ [^\(\n]*\(V[^J\n]*\(", txt3)
    # txt43 = re.findall("상기\([NM][A-Z][A-Z]{0,2}\) [^\n]{1,100}단계\([A-Z]", txt3)
    # print(txt41)
    # print(txt42[0])
    txt4 = []
    txt4b = []
    # for ln1 in txt41:
    #     txt4.append(re.sub(r" \/ 상기[^\n]*", "", ln1))
    # for ln1 in txt42:
    #     txt4.append(re.sub(r" \/ 상기[^\n]*", "", ln1))
    # for ln1 in txt43:
    #     txt4b.append(re.sub(r" \/ 상기[^\n]*", "", ln1))

    # print(txt2)
    # print(txt3)
    # print(txt4)

    slist = []
    slist5 = []
    sdic = dict()
    # sdic5 = dict()
    for l1 in txt41:
        buf5 = re.findall("\/ ([^\(]*)", l1)
        slist.append(buf5[0:-1])
    for l1 in txt42:
        buf5 = re.findall("\/ ([^\(]*)", l1)
        slist.append(buf5[0:-1])
    # for l1 in txt43:
    #     buf5 = re.findall("\/ ([^\(]*)", l1)
    #     slist5.append(buf5)

    slist.sort(key=len)
    # print(slist)
    for word in slist:
        wlen = len(word)
        tbuf = ""
        for i in range(wlen):
            if word[i] in ["사이", "중", ",", "서로", "내지", "이상", "보다"]:
                break
            tbuf = tbuf + word[i]
        if tbuf in sdic:
            sdic[tbuf] = sdic[tbuf] + 1
        else:
            sdic[tbuf] = 1
    slist5 = list(sdic.keys())
    slist=[]
    for wd in slist5:
        slist.append(re.sub("(?<=[가-힣])[\d][^\n]+", "", wd))
    slist.sort(key=len, reverse=True)


    for wt in slist:
        if len(wt) > 9 and wt[-2:] not in ["단계", "장치"]:
            bt = komoran.pos(wt)
            # print(wt) #디버그0 포인트
            for bbt in bt:
                if bbt[1] in ["XSA", "MAG", "XSV", "JC", "EC", "VA"]:
                    # print(wt)  # 디버그0 포인트
                    trash.append(wt)
                    slist.remove(wt)
                    break

    # slist5.sort(key=len)
    # # print(slist)
    # for word in slist5:
    #     wlen = len(word)
    #     tbuf = ""
    #     for i in range(wlen):
    #         if word[i] in ["또는", "및", ","]:
    #             break
    #         tbuf = tbuf + word[i]
    #     if tbuf in sdic5:
    #         sdic5[tbuf] = sdic5[tbuf] + 1
    #     else:
    #         sdic5[tbuf] = 1
    # slist5 = list(sdic5.keys())
    # slist5.sort(key=len, reverse=True)

    # print(slist5)
    slist3 = slist
    # print(slist)  # 디버그2 포인트
    # sdic = dict()
    slist1 = []
    slist4 = []
    for word in slist:
        flag = 0
        wlen = len(word)
        for i in range(int(wlen / 2) + 1):
            if word[:-(i + 1)] in slist:
                if len(word[:-(i + 1)]) == 1:
                    trash.append(word)
                    flag = 1
                    break
                if len(word[-(i + 1):]) == 1 and word[-(i + 1):] in exlist1:
                    flag = 0
                    break
                elif len(word[-(i + 1):]) == 2 and word[-(i + 1):] in exlist2:
                    flag = 0
                    break
                elif len(word[-(i + 1):]) == 3 and word[-(i + 1):] in exlist3:
                    flag = 0
                    break
                elif len(word[-(i + 1):]) == 4 and word[-2:] in ["튜브", "장치", "단계", "방향", "공간", "로봇", "통로", "모듈", "레버",
                                                                 "스터", "모터"]:
                    flag = 0
                    break
                elif len(word[-(i + 1):]) == 5 or len(word[-(i + 1):]) == 6:
                    for wrd2 in komoran.pos(word[-(i + 1):]):
                        if wrd2[1].startswith("N"):
                            # print(wrd2[0]) #디버그 포인트
                            flag = 0
                        else:
                            trash.append(word)
                            flag = 1
                            break
                        flag = 0
                    break
                else:
                    trash.append(word)
                    flag = 1
                    break
                flag = 1
        if flag == 0:
            slist1.append(word)
    # slist1.sort(key=len, reverse=True)
    buf=dict()
    for itt in slist1:
        if len(itt) >1 and len(itt) <6 and itt[-2:] !="단계":
            if itt in buf:
                buf[itt] = buf[itt] + 1
            else:
                buf[itt] = 1
    slist5 = list(buf.keys())
    # print(slist1)
    return slist5

def cut(tex1):
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

def cut2(tex1):
    string=tex1
    if string=="":
        return ""
    string = re.sub("\]삭제", "]", string)
    string = re.sub("\[청구항 [\d]{1,3}\]제[^서]{1,30}서", "", string)
    string = re.sub("\[청구항 [\d]+\]", "", string)
    string = re.sub("제[ ]{0,1}([\d]{1,3})[ ]{0,1}항[ 또에내지의중의]{1,4}", "", string)
    string = re.sub("제[ ]{0,2}[\d]{1,2}", " ", string)
    string = re.sub("\([^\)\(]{1,40}\)","",string) #괄호 날림
    string = re.sub("\([^\)\(]{1,40}\)", "", string)  # 괄호 날림
    string = re.sub("길이", "사이즈", string)
    string = re.sub("및", " ", string)
    string = re.sub("([^가-힣])상기", "\g<1> ", string)
    string = re.sub("([가-힣]+)[ ]{0,1}수단[\n으들은을이에의과 .]", "\g<1> 장치 ", string)
    string = re.sub("([가-힣]+)[ ]{0,1}모듈[\n으은들을이에의과 .]", "\g<1> 장치 ", string)
    string = re.sub("([가-힣]+)기구[\n로는를가들에의와 .]", "\g<1> 장치 ", string)
    string = re.sub("([가-힣]+) 기구[\n로는를들가에의와 .][^되된하한적]", " \g<1> 장치 ", string)
    string = re.sub("([가-힣]+)장비[\n로는를가에들의와 .]", "\g<1> 장치 ", string)
    string = re.sub("([가-힣]+) 장비[\n로는를가에들의와 .][^되된하한적]", " \g<1> 장치 ", string)
    string = re.sub("([가-힣]+)유닛[\n으은들을이에의과 .]", "\g<1> 장치 ", string)
    string = re.sub("([가-힣]{2,})부[\n로는를가에의들와 .]", "\g<1> 장치 ", string)
    string = re.sub("([가-힣]+) 부[\n로는를가에들의와 .][^되된하한적]", " \g<1> 장치 ", string)
    # string = re.sub("([가-힣]{2,})기[\n로는를가에의들와 .]", "\g<1> 장치 ", string)
    string = re.sub("[^가-힣ㄱ-ㅎa-zA-Z0-9\-%^.<>=/ ]", " ", string)

    string = re.sub("적어도 하나의", "", string)
    string = re.sub("적어도 하나", "", string)
    string = re.sub("[복수여러다\d]{1,3}[ ]{0,1}[개]{0,1}의", "", string)
    string = re.sub("[복수여러\d]{1,3}[ ]{0,1}개", "", string)
    string = re.sub("[ ]{2,}", " ", string)
    string = re.sub(" [에와과을를이가로] ", " ", string)
    return string

def par(flist, n):
    ln=len(flist)
    idx=n*60
    ddic=dict()
    pick = "[사전" + str(n) + "].pickle"
    for doc in flist:
        # print(ddic)
        print("%d\t%d"%(idx, len(ddic)))
        workbook = xlrd.open_workbook(doc)
        worksheet = workbook.sheet_by_index(0)
        nrows = worksheet.nrows
        for row_num in range(8, nrows):
            claim = worksheet.cell_value(row_num, 7)
            string = claim
            string = cut(string)
            # slist = said(string)
            # string = re.sub("[^가-힣]상기", "", string)
            txt1 = m.parse(string)
            txt = txt1.split("\n")
            # for we in slist:
            #     if we in ddic:
            #         ddic[we] = ddic[we] + 1
            #     else:
            #         ddic[we] = 1
            for word in txt:
                if len(word) > 5:
                    # print(word)
                    pos = word.split("\t")[1]
                    name = word.split("\t")[0]
                    name= re.sub("(?<=[가-힣])[\d][^\n]+", "", name)
                    if pos.startswith('N') or pos.startswith('SL') or pos.startswith('M'):
                        if name in ddic:
                            ddic[name] = ddic[name] + 1
                        else:
                            ddic[name] = 1
        idx=idx+1
    with gzip.open(pick, 'wb') as f:
        pickle.dump(ddic, f, pickle.HIGHEST_PROTOCOL)
    return

def bug(string):
    string = string.replace("F24J1/00", "F24V30/00")
    string = string.replace("F24J2/00", "F24S20/00")
    string = string.replace("F24J2/02", "F24S20/30")
    string = string.replace("F24J2/04", "F24S10/00")
    string = string.replace("F24J2/05", "F24S10/40")
    string = string.replace("F24J2/06", "F24S23/00")
    string = string.replace("F24J2/07", "F24S20/20")
    string = string.replace("F24J2/08", "F24S23/30")
    string = string.replace("F24J2/10", "F24S23/70")
    string = string.replace("F24J2/12", "F24S23/71")
    string = string.replace("F24J2/13", "F24S23/72")
    string = string.replace("F24J2/14", "F24S23/74")
    string = string.replace("F24J2/15", "F24S23/75")
    string = string.replace("F24J2/16", "F24S23/77")
    string = string.replace("F24J2/18", "F24S23/79")
    string = string.replace("F24J2/20", "F24S10/50")
    string = string.replace("F24J2/22", "F24S10/55")
    string = string.replace("F24J2/23", "F24S10/60")
    string = string.replace("F24J2/24", "F24S10/70")
    string = string.replace("F24J2/26", "F24S10/75")
    string = string.replace("F24J2/28", "F24S10/80")
    string = string.replace("F24J2/30", "F24S10/30")
    string = string.replace("F24J2/32", "F24S10/95")
    string = string.replace("F24J2/34", "F24S60/00")
    string = string.replace("F24J2/36", "F24S20/50")
    string = string.replace("F24J2/38", "F24S50/20")
    string = string.replace("F24J2/40", "F24S50/00")
    string = string.replace("F24J2/42", "F24S90/00")
    string = string.replace("F24J2/44", "F24S10/90")
    string = string.replace("F24J2/46", "F24S40/00")
    string = string.replace("F24J2/48", "F24S70/10")
    string = string.replace("F24J2/50", "F24S80/50")
    string = string.replace("F24J2/51", "F24S80/60")
    string = string.replace("F24J2/52", "F24S20/70")
    string = string.replace("F24J2/54", "F24S30/40")
    string = string.replace("F24J3/00", "F24V40/00")
    string = string.replace("F24J3/06", "F24V50/00")
    string = string.replace("F24J3/08", "F24T10/00")
    return string

def tf(flist, ipcdic, n):
    # ln=len(flist)
    # hit = [0] * 217775
    idx=n*86
    pick = "[CN][" + str(n) + "].pickle"
    # pick2 = "HIT[" + str(n) + "].pickle"
    fq = []
    te=list(ipcdic.keys())
    for doc in flist:
        # print(ddic)
        print("%d\t"%(idx))
        workbook = xlrd.open_workbook(doc)
        worksheet = workbook.sheet_by_index(0)
        nrows = worksheet.nrows
        for row_num in range(8, nrows):
            bufd = dict()
            buf1=[]
            buf2=[]
            string4 = re.sub("\([^|]+", "", worksheet.cell_value(row_num, 7))
            string4 = string4.replace(" ", "")
            string4.upper()
            if "F24J" in string4:
                string4=bug(string4)
            string5 = string4.split("|")
            for wrd in string5:
                if wrd in te:
                    buf1=buf1+ipcdic[wrd]
                else:
                    wrd2=re.sub("\/[^/]+","",wrd)
                    if wrd2 in te:
                        buf1 = buf1 + ipcdic[wrd2]+[wrd]
                    elif len(wrd2) >=4:
                        wrd3=wrd2[:4]
                        if wrd3 in te:
                            buf1 = buf1 + ipcdic[wrd3]+[wrd2]+[wrd]
                        else:
                            if wrd3 =="F24J":
                                buf1 = buf1 + ipcdic["F24S"]
                            print("시부럴 "+wrd3+" "+wrd2+" "+wrd)
            for wrd1 in buf1:
                if len(wrd1) >1:
                    if wrd1 in bufd:
                        bufd[wrd1]=bufd[wrd1]+1
                    else:
                        bufd[wrd1]=1
            # string3 = re.sub("\/[^|]+", "", worksheet.cell_value(row_num, 7))
            # string3 = string3.replace(" ","")
            # string3.upper()
            # string2 = string3.split("|")
            # for wrd in string2:
            #     if wrd in bufd:
            #         bufd[wrd]=bufd[wrd]+1
            #     else:
            #         bufd[wrd]=1
                # if wrd[:4] in bufd:
                #     bufd[wrd[:4]] = bufd[wrd[:4]] + 1
                # else:
                #     bufd[wrd[:4]] = 1
            buf1=list(bufd.keys())
            fq.append(buf1)
            # fq.append(re.sub("\([^\(]+", "", string))
            # string = cut(string)
            # slist = said(string)
            # string = re.sub("[^가-힣]상기", "", string)
            # txt1 = m.parse(string)
            # txt = txt1.split("\n")
            # for wrd1 in slist:
            #     if wrd1 in dic:
            #         buf.append(wrd1)
            # for word in txt:
            #     if len(word) > 5:
            #         # print(word)
            #         pos = word.split("\t")[1]
            #         name = word.split("\t")[0]
            #         name= re.sub("(?<=[가-힣])[\d][^\n]+", "", name)
            #         if pos.startswith('N') or pos.startswith('SL'):
            #             if name in dic:
            #                 buf.append(name)
            # for wrd in buf:
            #     buf1.append(dic.index(wrd))
            # counter = collections.Counter(buf1)
            # counter1 = counter.most_common()
            # fq.append(buf1)
            # for word in counter1:
            #     hit[word[0]] = hit[word[0]] + 1
        idx=idx+1
    with gzip.open(pick, 'wb') as f:
        pickle.dump(fq, f, pickle.HIGHEST_PROTOCOL)
    # with gzip.open(pick2, 'wb') as f:
    #     pickle.dump(hit, f, pickle.HIGHEST_PROTOCOL)
    return

def tf4(flist, n):
    # ln=len(flist)
    # hit = [0] * 217775
    idx=n*86
    pick = "IPC[파][" + str(n) + "].pickle"
    # pick2 = "HIT[" + str(n) + "].pickle"
    fq = []

    for doc in flist:
        # print(ddic)
        print("%d\t"%(idx))
        workbook = xlrd.open_workbook(doc)
        worksheet = workbook.sheet_by_index(0)
        nrows = worksheet.nrows
        for row_num in range(8, nrows):
            bufd = dict()
            buf1=[]
            buf2=[]
            string4 = re.sub("\([^|]+", "", worksheet.cell_value(row_num, 7))
            string4 = string4.replace(" ", "")
            string4.upper()
            if "F24J" in string4:
                string4=bug(string4)
            string5 = string4.split("|")
            for wrd in string5:
                if "/" in wrd and wrd in dst and wrd[-3:] !="/00":
                    # print(wrd)
                    ns=idic[wrd][4]
                    if ns in bufd:
                        bufd[ns]=bufd[ns]+1
                    else:
                        bufd[ns]=1
            buf1=list(bufd.keys())
            fq.append(buf1)
        idx=idx+1
    with gzip.open(pick, 'wb') as f:
        pickle.dump(fq, f, pickle.HIGHEST_PROTOCOL)
    # with gzip.open(pick2, 'wb') as f:
    #     pickle.dump(hit, f, pickle.HIGHEST_PROTOCOL)
    return

def tf3(flist, n):
    # ln=len(flist)
    # hit = [0] * 217775
    idx=n*111
    pick = "DBDB[" + str(n) + "].pickle"
    # pick2 = "HIT[" + str(n) + "].pickle"
    fq = []
    for doc in flist:
        # print(ddic)
        print("%d\t"%(idx))
        workbook = xlrd.open_workbook(doc)
        worksheet = workbook.sheet_by_index(0)
        nrows = worksheet.nrows
        for row_num in range(8, nrows):
            buf = []
            string1 = worksheet.cell_value(row_num, 1)
            string2= string1[3:7]
            buf.append(string1)
            buf.append(string2)
            for i in range(8):
                buf.append(worksheet.cell_value(row_num, i+4))
            fq.append(buf)
        idx=idx+1
    with gzip.open(pick, 'wb') as f:
        pickle.dump(fq, f, pickle.HIGHEST_PROTOCOL)
    # with gzip.open(pick2, 'wb') as f:
    #     pickle.dump(hit, f, pickle.HIGHEST_PROTOCOL)
    return

def tf2(flist, dic, n):
    ln=len(flist)
    idx=n*110
    title = str(n) + ".txt"
    g = open(title, "w", encoding="utf-8")
    for doc in flist:
        # print(ddic)
        print("%d\t"%(idx))
        workbook = xlrd.open_workbook(doc)
        worksheet = workbook.sheet_by_index(0)
        nrows = worksheet.nrows
        for row_num in range(8, nrows):
            bufs=""
            claim = worksheet.cell_value(row_num, 6)
            string = claim
            string = cut(string)
            string = re.sub("[^가-힣]상기", "", string)
            txt1 = m.parse(string)
            txt = txt1.split("\n")
            for word in txt:
                if len(word) > 5:
                    # print(word)
                    pos = word.split("\t")[1]
                    name = word.split("\t")[0]
                    name= re.sub("(?<=[가-힣])[\d][^\n]+", "", name)
                    if pos.startswith('N') or pos.startswith('SL') or pos.startswith('M'):
                        if name in dic:
                            bufs=bufs+" "+name
            if bufs=="":
                bufs="none"
            g.write(bufs)
            g.write("\n")
        idx = idx + 1
    g.close()
    return

def fqf():
    fq=[]
    for i in range(9):
        print(i)
        txt = "FQ[" + str(i) + "].pickle"
        f2 = gzip.open(txt, 'rb')
        f1 = pickle.load(f2)
        fq=fq+f1
        f2.close()
    return fq

def hitf():
    hit = [0] * 217775
    for i in range(9):
        print(i)
        txt = "HIT[" + str(i) + "].pickle"
        f2=gzip.open(txt, 'rb')
        f1=pickle.load(f2)
        for i in range(len(hit)):
            hit[i]=hit[i]+f1[i]
        f2.close()
    return hit

def tos(list1):
    temp = []
    for wrd in list1:
        temp.append(str(wrd))
    return temp


def ui(string):
    n1 = dic.index(string)
    list1 = model.wv.most_similar(str(n1), topn=20)
    for i, v in list1:
        print("%s\t\t유사도: %f" % (dic[int(i)], v))
    return


def io(string):
    n1 = dic.index(string)
    return str(n1)

if __name__ == "__main__":
    path = "C:/Users/User/PycharmProjects/patent/newdb/*"
    # path = "C:/DB/DB/*"
    file_list = glob.glob(path)
    f_list = [file for file in file_list if file.endswith(".xls")]
    # f1 = gzip.open("사전(정리).pickle", 'rb')
    # dic = pickle.load(f1)
    # f1.close()
    # f1 = gzip.open("CPC.pickle", 'rb')
    # cpc = pickle.load(f1)
    # f1.close()
    # f1 = gzip.open("DBDB.pickle", 'rb')
    # DB = pickle.load(f1)
    # f1.close()
    # f1 = gzip.open("IPCTREE.pickle", 'rb')
    # IPTREE = pickle.load(f1)
    # f1.close()
    # ipidx=[]
    # for lst in IPTREE:
    #     ipidx.append(lst[-1])
    #
    # IPdic=dict()
    #
    # for i in range(len(ipidx)):
    #     IPdic[ipidx[i]]=IPTREE[i]
    # f1 = gzip.open("IPC사전.pickle", 'rb')
    # IPdic = pickle.load(f1)
    # f1.close()

    # f1 = gzip.open("출원번호.pickle", 'rb')
    # CN = pickle.load(f1)
    # f1.close()

    # for wrd in CN[:2000]:
    #     print(wrd, end="")
    #     print("+", end="")
    # print("\n")
    # cplist=["A01B", "A01C", "A01D", "A01F", "A01G", "A01H", "A01J", "A01K", "A01L", "A01M", "A01N", "A21B", "A21C", "A21D", "A22B", "A22C", "A23B", "A23C", "A23D", "A23F", "A23G", "A23J", "A23K", "A23L", "A23B", "A23J", "A23N", "A23P", "A23V", "A23Y", "A24B", "A24C", "A24D", "A24F", "A41B", "A41C", "A41D", "A41F", "A41G", "A41H", "A42B", "A42C", "A43B", "A43C", "A43D", "A44B", "A44C", "A44D", "A45B", "A45C", "A45D", "A45F", "A46B", "A46D", "A47B", "A47C", "A47D", "A47F", "A47G", "A47H", "A47J", "A47K", "A47L", "A61B", "A61C", "A61D", "A61F", "A61G", "A61H", "A61J", "A61K", "A61L", "A61M", "A61N", "A61P", "A61Q", "A62B", "A62C", "A62D", "A63B", "A63C", "A63D", "A63F", "A63G", "A63H", "A63J", "A63K", "A99Z", "B01B", "B01D", "B01F", "B01J", "B01L", "B02B", "B02C", "B03B", "B03C", "B03D", "B04B", "B04C", "B05B", "B05C", "B05D", "B06B", "B07B", "B07C", "B08B", "B09B", "B09C", "B21B", "B21C", "B21D", "B21F", "B21G", "B21H", "B21J", "B21K", "B21L", "B22C", "B22D", "B22F", "B23B", "B23C", "B23D", "B23F", "B23G", "B23H", "B23K", "B23P", "B23Q", "B24B", "B24C", "B24D", "B25B", "B25C", "B25D", "B25F", "B25G", "B25H", "B25J", "B26B", "B26D", "B26F", "B27B", "B27C", "B27D", "B27F", "B27G", "B27H", "B27J", "B27K", "B27L", "B27M", "B27B", "B27L", "B27N", "B28B", "B28C", "B28D", "B29B", "B29C", "B29D", "B29K", "B29D", "B29L", "B29C", "B30B", "B31B", "B31C", "B31D", "B31B", "B31C", "B31F", "B32B", "B33Y", "B41B", "B41C", "B41D", "B41F", "B41G", "B41J", "B41K", "B41L", "B41M", "B41N", "B41P", "B42B", "B42C", "B42D", "B42F", "B42P", "B43K", "B43L", "B43M", "B44B", "B44C", "B44D", "B44F", "B60B", "B60C", "B60D", "B60F", "B60G", "B60H", "B60J", "B60K", "B60L", "B60M", "B60N", "B60P", "B60Q", "B60R", "B60S", "B60T", "B60V", "B60W", "B60Y", "B61B", "B61C", "B61D", "B61F", "B61G", "B61H", "B61J", "B61K", "B61L", "B62B", "B62C", "B62D", "B62H", "B62J", "B62K", "B62L", "B62M", "B63B", "B63C", "B63G", "B63H", "F42B", "B63J", "B64B", "B64C", "B64D", "B64F", "B64G", "B65B", "F42B", "B65D", "B65F", "B65G", "B65H", "B66B", "B66C", "B66D", "B66F", "B67B", "B67C", "B67D", "B68B", "B68C", "B68F", "B68G", "B81B", "B81C", "B82B", "B82Y", "B99Z", "C01B", "C01C", "C01D", "C01F", "C01G", "C01D", "C01F", "C01P", "C02F", "C03B", "C03C", "C04B", "C05B", "C05C", "C05D", "C05B", "C05C", "C05F", "C05B", "C05C", "C05G", "C06B", "C06C", "C06D", "C06F", "C07B", "C07C", "C07D", "C07F", "C07G", "C07H", "C07J", "C07K", "C08B", "C08C", "C08F", "C08G", "C08H", "C08J", "C08B", "C08C", "C08F", "C08G", "C08K", "C08L", "C09B", "C09C", "C09D", "C09F", "C09G", "C09H", "C09J", "C09K", "C10B", "C10C", "C10F", "C10G", "C10H", "C10J", "C10K", "C10L", "C10G", "C10K", "C10M", "C10N", "C10M", "C11B", "C11C", "C11D", "C12C", "C12F", "C12G", "C12G", "C12C", "C12H", "C12H", "C12J", "C12L", "C12M", "C12N", "C12P", "C12Q", "C12R", "C12Y", "C13B", "C13K", "C14B", "C14C", "C21B", "C21C", "C21D", "C22B", "C22C", "C22F", "C23C", "C23D", "C23F", "C21D", "C23G", "C25B", "C25C", "C25D", "C25F", "C30B", "C40B", "C99Z", "C01B", "C01C", "C01D", "C01F", "C01G", "C01D", "C01F", "C01P", "C02F", "C03B", "C03C", "C04B", "C05B", "C05C", "C05D", "C05B", "C05C", "C05F", "C05B", "C05C", "C05G", "C06B", "C06C", "C06D", "C06F", "C07B", "C07C", "C07D", "C07F", "C07G", "C07H", "C07J", "C07K", "C08B", "C08C", "C08F", "C08G", "C08H", "C08J", "C08B", "C08C", "C08F", "C08G", "C08K", "C08L", "C09B", "C09C", "C09D", "C09F", "C09G", "C09H", "C09J", "C09K", "C10B", "C10C", "C10F", "C10G", "C10H", "C10J", "C10K", "C10L", "C10G", "C10K", "C10M", "C10N", "C10M", "C11B", "C11C", "C11D", "C12C", "C12F", "C12G", "C12G", "C12C", "C12H", "C12H", "C12J", "C12L", "C12M", "C12N", "C12P", "C12Q", "C12R", "C12Y", "C13B", "C13K", "C14B", "C14C", "C21B", "C21C", "C21D", "C22B", "C22C", "C22F", "C23C", "C23D", "C23F", "C21D", "C23G", "C25B", "C25C", "C25D", "C25F", "C30B", "C40B", "C99Z", "D01B", "D01C", "D01D", "D01F", "D01G", "D01H", "D02G", "D02H", "D02J", "D03C", "D03D", "D03J", "D04B", "D04C", "D04D", "D04G", "D04H", "D05B", "D05C", "D05D", "D05B", "D05C", "D06B", "D06C", "D06F", "D06G", "D06H", "D06J", "D06L", "D06M", "D06N", "D06P", "D06Q", "D07B", "D10B", "D21B", "D21C", "D21D", "D21F", "D21G", "D21H", "D21C", "D21D", "D21G", "D21J", "D99Z", "E01B", "E01C", "E01D", "E01F", "E01H", "E02B", "E02C", "E02D", "E02F", "E03B", "E03C", "E03D", "E03F", "E04B", "E04C", "E04D", "E04F", "E04G", "E04H", "E05B", "E05C", "E05D", "E05F", "E05G", "E05Y", "E06B", "E06C", "E21B", "E21C", "E21D", "E21F", "E99Z", "F01B", "F01C", "F01D", "F01K", "F01L", "F01M", "F01N", "F01P", "F02B", "F02C", "F02D", "F02F", "F02G", "F02K", "F02M", "F02N", "F02P", "F03B", "F03C", "F03D", "F03G", "F03H", "F04B", "F04C", "F04D", "F04F", "F05B", "F05C", "F05D", "F15B", "F15C", "F15D", "F16B", "F16C", "F16D", "B61H", "B62L", "F16F", "F16G", "F16H", "F16J", "F16K", "F16L", "F16M", "F16N", "F16P", "F16S", "F16T", "F17B", "F17C", "F17D", "F21H", "F21K", "F21L", "F21S", "F21V", "F21W", "F21K", "F21L", "F21S", "F21V", "F21Y", "F21K", "F21L", "F21S", "F21V", "F22B", "F22D", "F22G", "F23B", "F23C", "F23D", "F23G", "F23H", "F23J", "F23K", "F23L", "F23M", "F23N", "F23Q", "F23R", "F24B", "F24C", "F24D", "F24F", "F24H", "F24S", "F24T", "F24V", "F25B", "F25C", "F25D", "F25J", "F26B", "F27B", "F27D", "F27M", "F28B", "F28C", "F28D", "F28F", "F28G", "F41A", "F41B", "F41C", "F41F", "F41G", "F41H", "F41J", "F42B", "F42C", "F42D", "F99Z", "G01B", "G01C", "G01D", "G01F", "G01G", "G01H", "G01J", "G01K", "G01L", "G01M", "G01N", "G01P", "G01Q", "G01R", "G01S", "G01T", "G01V", "G01W", "G02B", "G02C", "G02F", "G03B", "G03C", "G03D", "G03F", "G03G", "G03H", "G04B", "G04C", "G04D", "G04F", "G04G", "G04R", "G05B", "G05D", "G05F", "G05G", "G06C", "G06D", "G06E", "G06F", "G06G", "G06J", "G06K", "G06M", "G06N", "G06Q", "G06T", "G07B", "G07C", "G07D", "G07F", "G07G", "G08B", "G08C", "G08G", "G09B", "G09C", "G09D", "G09F", "G09G", "G10B", "G10C", "G10D", "G10F", "G10G", "G10H", "G10K", "G10L", "G11B", "G11C", "G12B", "G16B", "G16C", "G16H", "G16Y", "G16Z", "G21B", "G21C", "G21D", "G21F", "G21G", "G21H", "G21J", "G21K", "G99Z", "H01B", "H01C", "H01F", "H01G", "H01H", "H01J", "H01K", "H01L", "H01M", "H01P", "H01Q", "H01R", "H01S", "H01T", "H02B", "H02G", "H02H", "H02J", "H02K", "H02M", "H02N", "H02P", "H02S", "H03B", "H03C", "H03D", "H03F", "H03G", "H03H", "H03J", "H03K", "H03L", "H03M", "H04B", "H04H", "H04J", "H04K", "H04L", "H04M", "H04N", "H04Q", "H04R", "H04S", "H04T", "H04W", "H05B", "H05C", "H05F", "H05G", "H05H", "H05K", "H99Z", "Y02A", "Y02B", "Y02C", "Y02D", "Y02E", "Y02P", "Y02T", "Y02W", "Y04S", "Y10S", "Y10T", "Z01B", "Z01C", "Z01I", "Z01T", "Z03A", "Z03C", "Z03D", "Z03H", "Z03M", "Z03R", "Z03V", "Z05E", "Z05M", "Z05P", "Z05S"]
    # tk=[]
    # for i in range(9):
    #     print(i)
    #     txt = "INF[" + str(i) + "].pickle"
    #     f1=gzip.open(txt, 'rb')
    #     tk=tk+pickle.load(f1)
    #     f1.close()
    #
    # model = gensim.models.doc2vec.Doc2Vec.load("doc2vec[라].model")
    # wrd = dic.most_common()
    # wrd1 = sorted(wrd, key=itemgetter(1), reverse=False)
    # wrd2 = wrd[:100000]
    # g = open("사전점검.txt", "w", encoding="utf-8")
    # for wo in wrd2:
    #     g.write(wo[1])
    #     g.write("\t")
    #     g.write(str(wo[2]))
    #     g.write("\n")
    # g.close()


    # cnt=0
    # for wrd in sorted_C:
    #     print(cnt)
    #     if wrd[1] == 10:
    #         break
    #     cnt=cnt+1
    #
    # nlist = sorted_C[cnt:]
    # nlist = sorted(nlist, key=itemgetter(1), reverse=True)
    #
    # dic = []
    # for wrd in nlist:
    #     dic.append(wrd[0])
    # #
    # with gzip.open('CPlist.pickle', 'wb') as f:
    #     pickle.dump(cclist, f, pickle.HIGHEST_PROTOCOL)

    j = 10
    l = int(860 / j)
    v=[]
    for i in range(j):
        x = int(i * l)
        y = int((i + 1) * l)
        v.append(Process(target=tf4, args=(f_list[x:y], i)))
        # v.append(Process(target=tf, args=(f_list[x:y], IPdic, i)))
        # v.append(Process(target=sims, args=(i, tk[x:y], model)))
    # v.append(Process(target=tf, args=(f_list[880:888], dic, 8)))
    for th in v:
        th.start()
    for th in v:
        th.join()
    print("종료")
    #
    IPC=[]
    # # ddic=dict()
    for i in range(10):
        print(i)
        txt = "IPC[파][" + str(i) + "].pickle"
        f1=gzip.open(txt, 'rb')
        IPC=IPC+pickle.load(f1)
        f1.close()
    with gzip.open('IPC[파].pickle', 'wb') as f:
        pickle.dump(IPC, f, pickle.HIGHEST_PROTOCOL)

    # for lst in DB:
    #     print(DB5.index(lst[0]))
    #
    #
    # CPC=[]
    # count=0
    # for num in CN3:
    #     if count%1000 ==0:
    #         print(count)
    #     count=count+1
    #     if num not in SET3:
    #         CP=DB5[CN2.index(num)][6]
    #         CPC.append(CP)
    #     else:
    #         CPC.append("")

    #
    # c=0
    # IPDICT=dict()
    # for doc in IPTRR:
    #     if c%100 ==0:
    #         print(c)
    #     c=c+1
    #     for tag in doc:
    #         if tag in IPDICT:
    #             IPDICT[tag]=IPDICT[tag]+1
    #         else:
    #             IPDICT[tag]=1
    #
    # IPLST=list(IPDICT.itmes())
    # IPLST2 = sorted(IPLST, key=itemgetter(1), reverse=False)

    # # s=""
    # # tu=[]
    # g = open("TIlist.txt", "w", encoding="utf-8")
    # for doc in tk:
    #     g.write(doc)
    #     g.write("\n")
    # g.close()
    # for i,doc in enumerate(tk):
    #     s=""
    #     tdic=dict()
    #     # s = ' '.join(str(x) for x in doc)
    #     tu=doc.split("|")
    #     for unit in tu:
    #         if unit[:3] in tdic:
    #             tdic[unit[:3]]=tdic[unit[:3]]+1
    #         else:
    #             tdic[unit[:3]] = 1
    #     c=list(tdic.keys())
    #     if len(c) != 0:
    #         s = " ".join(c)
    #     g.write(s)
    #     g.write("\n")
    #     print(i)
    # g.close()
    #

    # dic2=[]
    # for i in range(10):
    #     dic2.append(collections.Counter(dic1[i]))
    # dic3=dic2[0]+dic2[1]+dic2[2]+dic2[3]+dic2[4]+dic2[5]+dic2[6]+dic2[7]+dic2[8]
    #
    # with open('사전(3M).pickle', 'wb') as f:
    #     pickle.dump(dic3, f, pickle.HIGHEST_PROTOCOL)
    # w3 = []
    # w5 = []
    # w6 = []
    # word3=[]
    # ddic1=dict()
    # for word2 in ddic.keys():
    #     word4=re.sub("제[\d]{1,2}", "", word2)
    #     word4=re.sub("[^가-힣]","",word4)
    #     if len(word4) > 2 and len(word4) <7:
    #         if word4 in ddic1:
    #             ddic1[word4]=ddic1[word4]+1
    #         else:
    #             ddic1[word4]=1
    #
    # word3=list(ddic1.keys())
    # for word5 in word3:
    #     if len(word5) == 3:
    #         w3.append(word5)
    #     elif len(word5) == 5:
    #         w5.append(word5)
    #     elif len(word5) == 6:
    #         w6.append(word5)
    #     else:
    #         continue
    #
    # word3.sort(key=len, reverse=False)
    # print(len(word3))
    #
    # w2=snoun1(w3, w5)
    # t1=snoun(word3)
    # print(len(t1))
    #
    # f2=open("sample1.txt", "r", encoding="utf-8")
    #
    # with open("sample2.txt", 'w', encoding="utf-8") as g:
    #     for i in range(7719):
    #         string2=f2.readline()[:-1]
    #         string3=m.parse(string2)
    #         g.write(string2)
    #         g.write("\n")
    #         g.write(string3)
    #         g.write("\n")
    #     g.close()

    # par(f_list[880:888], 8)



    # with gzip.open("FQ[new].pickle", 'wb') as f:
    #     pickle.dump(fq, f, pickle.HIGHEST_PROTOCOL)
    # with gzip.open("HIT[new].pickle", 'wb') as f:
    #     pickle.dump(hit, f, pickle.HIGHEST_PROTOCOL)
    # with gzip.open("TFIDF[new].pickle", 'wb') as f:
    #     pickle.dump(hit, f, pickle.HIGHEST_PROTOCOL)
    # with gzip.open("B[new].pickle", 'wb') as f:
    #     pickle.dump(b, f, pickle.HIGHEST_PROTOCOL)

    # f1 = gzip.open("사전(정리).pickle", 'rb')
    # dic = pickle.load(f1)
    # f1.close()
    # f1=gzip.open("HIT[new].pickle", 'rb')
    # hit=pickle.load(f1)
    # f1.close()
    # f2=gzip.open("B[new].pickle", 'rb')
    # tfidf=pickle.load(f2)
    # f2.close()
    #     dic1.append(pickle.load(f1))

    # log = []
    # for n in range(len(dic)):
    #     log.append(round(math.log10(4435880/(hit[n]+1)), 6))

    # tfidf = []
    # c=0
    # for line in fq:
    #     print(c)
    #     v1 = []
    #     for pair in line:
    #         v1.append([pair[0], round(pair[1] * log[pair[0]], 6)])
    #         c=c+1
    #     tfidf.append(v1)
    # cpc1=[]
    #
    # cdic2=dict()
    # for doc in cpc:
    #     cdic1 = dict()
    #     for item in doc:
    #         if item in cdic1:
    #             cdic1[item]=cdic1[item]+1
    #         else:
    #             cdic1[item]=0
    #     slist = list(cdic1.keys())
    #     cpc1.append(slist)
    #     for item in slist:
    #         if item in cdic2:
    #             cdic2[item]=cdic2[item]+1
    #         else:
    #             cdic2[item]=0
    #
    # wrd3 = collections.Counter(cdic2)
    # wrd=wrd3.most_common()
    # # slist2=list(cdic.keys())
    # # wrd1 = sorted(wrd, key=itemgetter(1), reverse=False)
    #
    # wrd4 = wrd[:-20]
    # cpclist = []
    # cclist=[]
    # for item in wrd4:
    #     cpclist.append(item[0])
    # #
    # # f2 = open("CPlist.txt", "w", encoding="utf-8")
    # cclist = []
    # for doc in cpc1:
    #     buf=[]
    #     for item in doc:
    #         if item in cpclist:
    #             buf.append(cpclist.index(item))
    #     if len(buf)!=0:
    #         cclist.append(cpclist[min(buf)])
    #     else:
    #         cclist.append("")