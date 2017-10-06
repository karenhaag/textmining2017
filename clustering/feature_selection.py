import pickle
from itertools import islice
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.feature_selection import chi2
import numpy as np
from sklearn.cluster import KMeans
from sklearn.feature_extraction import DictVectorizer
from sklearn.decomposition import TruncatedSVD

def not_is_int(s):
    try: 
        int(s)
        return False
    except ValueError:
        return True
def before_w(sent, i):
    if i!= 0:
        return sent[i-1][0]
    else:
        return "[start]"

def after_w(sent, i):
    if i < len(sent)-1:
        return sent[i+1][0]
    else:
        return "[end]"

def before_P(sent,i):
    if i!= 0:
        return sent[i-1][2]
    else:
        return "[start]"

def after_P(sent, i):
    if i < len(sent)-1:
        return sent[i+1][2]
    else:
        return "[end]"

def before_s(sent,i):
    if i!= 0:
        return sent[i-1][3]
    else:
        return "[start]"

def after_s(sent, i):
    if i < len(sent)-1:
        return sent[i+1][3]
    else:
        return "[end]"

def dic_pos(sentences):
    wordsDic = {}
    index_words = []
    list_context = []
    list_class = []
    count = 0
    for sent in sentences:
            for i,w in enumerate(sent):
                word = w[0]
                lemma_word = w[1]
                POS_word = w[2]
                synset_word = w[3]

                before_word = before_w(sent,i)
                before_POS = before_P(sent,i)
                before_synset = before_s(sent,i)
                after_word = after_w(sent,i)
                after_POS = after_P(sent,i)
                after_synset = after_s(sent,i)

                if wordsDic.get(word, None) == None:
                    lenDic = len(wordsDic)
                    wordsDic[word] = lenDic
                    index_words.append(word)
                    list_context.append({"lemma_word="+ lemma_word:1 , "synset_word="+synset_word:1, 
                                        "before_word="+before_word:1, "before_POS="+before_POS:1, 
                                        "before_synset="+before_synset:1,"after_word="+after_word:1, 
                                        "after_POS="+after_POS:1, "after_synset="+after_synset:1 })
                    list_class.append(POS_word)
                else: 
                    index = wordsDic[word]
                    list_context_aux = ["lemma_word="+ lemma_word,"synset_word="+synset_word, "before_word="+before_word,
                               "before_POS="+before_POS, "before_synset="+before_synset, "after_word="+after_word,
                               "after_POS="+after_POS, "after_synset="+after_synset]
                    for context in list_context_aux:
                        if list_context[index].get(context,None) == None:
                            list_context[index][context] = 1
                        else:
                            list_context[index][context] += 1
    return(wordsDic, index_words, list_context,list_class)

def get_sentences(head):
    sent = []
    for s in head:
        sent.append(s.split())
    words = []
    sentences = []
    for s in sent:
        if len(s) == 4 and not_is_int(s[0]) and  s[0] not in {'(', ')', ',', ';', ':', "'", "-", "_"} and '[' not in s[1]:
            words.append((s[0], s[1], s[2], s[3]))
    count = dict()
    for fst,snd,trd, fth in words:
        if fst not in count:
            count[fst] = 1
        else:
            count[fst] += 1
    aux = []
    check = []
    for fst,snd,trd, fth in words:
        aux.append((fst,snd,trd, fth))
        if fst == '.':
            check.append(aux)
            aux = []
    return(check)

def supervisado():
    svd = TruncatedSVD(n_components=47, n_iter=7, random_state=42)
    filename = "final.txt"
    with open(filename) as myfile:
        head = list(islice(myfile, 10000))
    check = get_sentences(head)
    wordsDic, index_words, list_context,list_class = dic_pos(check)
    v = DictVectorizer(sparse=True)
   
    X_normal = v.fit_transform(list_context)
   
    X_reducida_no_sup= svd.fit_transform(X_normal)
    y = list_class
   
    X_reducida_sup = SelectKBest(chi2, k=5).fit_transform(X_normal, y)
   
    kmeans_reducida_normal = KMeans(n_clusters=30, random_state=0).fit(X_normal)
    kmeans_reducida_sup = KMeans(n_clusters=30, random_state=0).fit(X_reducida_sup)
    kmeans_reducida_no_sup = KMeans(n_clusters=30, random_state=0).fit(X_reducida_no_sup)
    return(kmeans_reducida_normal, kmeans_reducida_no_sup, kmeans_reducida_sup, index_words)

def print_cluster_number(number, labels, index_words):
    print("------------------------------")
    print("CLUSTER : " + str(number))
    for t in enumerate (labels):
        if(t[1] == number):
            print (index_words[t[0]])

