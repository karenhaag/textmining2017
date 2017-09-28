import nltk
import numpy as np
import re
from nltk.corpus import PlaintextCorpusReader
from nltk.tokenize import RegexpTokenizer
from scipy.sparse import dok_matrix
from nltk.corpus import stopwords
from sklearn.cluster import KMeans
from nltk.tag.stanford import StanfordPOSTagger
from sklearn.feature_extraction import DictVectorizer

lemmaDict = {}
with open('lemmatization-es.txt', 'rb') as f:
    data = f.read().decode('utf8').replace(u'\r', u'').split(u'\n')
    data = [a.split(u'\t') for a in data]
for a in data:
    if len(a) >1:
        lemmaDict[a[1]] = a[0]


#Devuelve una lista de oraciones y lista de palabras
def tokenize(text, clean_stopwords):
    punctuation = re.compile(r'[-.?!,":;()|0-9]')    
    pattern = r'''(?ix)    # set flag to allow verbose regexps
     (?:[A-Z]\.)+        # abbreviations, e.g. U.S.A.
   | \w+(?:-\w+)*        # words with optional internal hyphens
   | \$?\d+(?:\.\d+)?%?  # currency and percentages, e.g. $12.40, 82%
   | \.\.\.            # ellipsis
   | [][.,;"'?():-_`]  # these are separate tokens; includes ], [
    '''
    tokenizer = RegexpTokenizer(pattern)
    corpus = PlaintextCorpusReader('.', text, word_tokenizer=tokenizer)
    sents_corpus = corpus.sents()
    print("cantidad de oraciones: ", len(sents_corpus))
    words_corpus = corpus.words()

    aux_sents = []
    for sent in sents_corpus:
        aux_sents.append([punctuation.sub("", word) for word in sent])
        aux_sents[len(aux_sents)-1] = list(filter(None, aux_sents[len(aux_sents)-1]))
    sents_corpus = aux_sents
    words_corpus = [punctuation.sub("", word) for word in words_corpus]     
    words_corpus = list(filter(None, words_corpus))    
    if clean_stopwords :
        stop = stopwords.words('spanish')
        aux_sents = []
        for sent in sents_corpus:
                aux_sents.append([w for w in sent if w not in stop])
        sents_corpus = aux_sents
        words_corpus = [w for w in words_corpus if w not in stop]
    return (sents_corpus, words_corpus)

#lemmatiza las palabras
def lemmatize(word):
    return lemmaDict.get(word, word) # + u'*'

#Construye la matriz de contextos
def matriz_construct_ctx1(dicWords, sentences):
    len_dic = len(dicWords)
    m = dok_matrix((len_dic,len_dic))
    for sent in sentences:    
        length_sent = len(sent)        
        for i_word in range(0,length_sent-1):
            w = lemmatize( sent[i_word].lower())
            w_pos = lemmatize( sent[i_word+1].lower())
            m[dicWords[w], dicWords[w_pos]] +=1
    return(m)

#Construye la matriz de 2 contextos
def matriz_construct_ctx2(dicWords, sentences):
    len_dic = len(dicWords)
    m = dok_matrix((len_dic,len_dic))
    for sent in sentences:    
        length_sent = len(sent)        
        for i_word in range(0,length_sent-2):
            w = lemmatize( sent[i_word].lower())
            w_pos1 = lemmatize( sent[i_word+1].lower())
            w_pos2 = lemmatize( sent[i_word+2].lower())
            m[dicWords[w], dicWords[w_pos1]] +=1
            m[dicWords[w_pos1], dicWords[w_pos2]] +=1  
            if i_word+2 == length_sent:        
                m[dicWords[w_pos1], dicWords[w_pos2]] +=1            
    return(m)



def tag_word(word_pos, word):
    return(word_pos.get(word, "None"))

#solucion temporal
def dic_pos(word_pos):
    d = {}
    l_d = []
    for w in word_pos.keys():
        if d.get(word_pos.get(w),"a") == "a":
            lend = len(d)
            d[word_pos.get(w)] = lend
            l_d.append(word_pos.get(w))
    lend = len(d)
    d["[start]"] = lend
    d["[end]"] = lend+1
    return(d,l_d)


def matriz_construct_pos(sents_corpus, words_pos,dicWords):
    d_pos, ind_dic_pos = dic_pos(words_pos)
    len_word_pos = len(words_pos)
    m = dok_matrix((len_word_pos,len(d_pos)))    

    for sent in sents_corpus:
        for i in range(len(sent)-1):
            w = sent[i]

            wb = w_before(sent, i)
            t_wb = tag_word(words_pos, wb)

            wa = w_after(sent, i)
            t_wa = tag_word(words_pos, wa)
            m[dicWords.get(w,0),d_pos.get(t_wb, 0)] +=1
            m[dicWords.get(w,0),d_pos.get(t_wa, 0)] +=1
    return(m)

def w_before(sent, i):
    if i!= 0:
        return sent[i-1]
    else:
        return "[start]"

def w_after(sent, i):
    if i < len(sent):
        return sent[i+1]
    else:
        return "[end]"

def dic_word_pos(dicWords):
    print("Creando dic_word_pos")    
    dic =  {}
    path_to_jar = "/home/karen/text_mining/stanford-postagger-full-2017-06-09/stanford-postagger-3.8.0.jar"
    path_to_model = "/home/karen/text_mining/stanford-postagger-full-2017-06-09/models/spanish-distsim.tagger"
    tagger = StanfordPOSTagger(path_to_model, path_to_jar)
    print("creando taggers")        
    aux = tagger.tag(dicWords.keys())
    print("creando diccionario")            
    for a in aux :
        dic[a[0]] = a[1]
    print("termino crear dic")            
    return(dic)

def dic_construct(words, lemm):
    dicWords = {} #diccionario que tiene clave: palabra, value: index en la lista
    list_index = [] #Lista de indices
    for word in words:
        if lemm: 
            w = lemmatize( word.lower()) #Lematiza
        else:
            w = word.lower()
        if dicWords.get(w, -1) < 0: #no esta en dic
            len_dic = len(dicWords)
            dicWords[w] = len_dic
            list_index.append(w)
    return(dicWords, list_index)

#inicializa todo lo necesario para el entrenamiento
def inicialize(text, clean_text, option, lemm=True):
    print("inicicalizando")
    #todas las palabras y las oraciones del corpus
    sents_corpus, word_corpus = tokenize(text, clean_text)
    #dicWords =  todas las palabras del corpus
    check_list = []
    dicWords, list_index = dic_construct(word_corpus, lemm)
    if option == 1:
        m = matriz_construct_ctx1(dicWords, sents_corpus)
    if option == 2: 
        m = matriz_construct_ctx2(dicWords, sents_corpus) 
    if option == 3:
        print("opcion 3")
        d_words_pos = dic_word_pos(dicWords)
        print ("termino lo peor")
        m = matriz_construct_pos(sents_corpus, d_words_pos,dicWords)         
    return(sents_corpus, word_corpus,dicWords, list_index, m)

#Entrenamiento kmeans
def clusters(n_clusters, m):
   return (KMeans(n_clusters=n_clusters, random_state=0).fit(m))

#IMprime los clusters y las palabras asociadas a cada cluster
def print_clusters(clusters_n, labels, list_index):
    for i in range(clusters_n):
        print("-----------------------------")
        print("CLUSTER: " , i)
        for t in enumerate (labels):
            if(t[1] == i):
                print (list_index[t[0]])
        
#Para ejecutar:
# text = "lavoztextodump.txt" 
# clen_stopwords = True (Setear en true si se quiere un corpus sin stopwords, False caso contrario)       
# sents_corpus, word_corpus,dicWords, list_index, m = clustering.inicialize(text, clean_stopwords)
# n_clusters = 3 (setear cantidad de clusters que quieras)
# kmeans = clusters(n_clusters, m)
# labels = kmeans.labels_
# print_clusters(n_clusters, labels, list_index)