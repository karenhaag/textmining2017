import re
from nltk.corpus import PlaintextCorpusReader
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords

#Load a lictionari of spanish lemmas
def load_lemmaDict():
    lemmaDict = {}
    with open('lemmatization-es.txt', 'rb') as f:
        data = f.read().decode('utf8').replace(u'\r', u'').split(u'\n')
        data = [a.split(u'\t') for a in data]
    for a in data:
        if len(a) >1:
            lemmaDict[a[1]] = a[0]
    return(lemmaDict)

def lemmatize(word, lemmaDict):
    punctuation = re.compile(r'[-.?!,":;()|0-9]')            
    w = punctuation.sub("", word).lower()
    return lemmaDict.get(w, w) 

#input: list of sents and list of words, return the sames lists but without puntuations signs
def clean_sents_words(sents_corpus, lemmaDict):
    aux_sents = []
    for sent in sents_corpus:
        aux_sents.append([lemmatize(word, lemmaDict) for word in sent])
        aux_sents[len(aux_sents)-1] = list(filter(None, aux_sents[len(aux_sents)-1]))
    sents_corpus = aux_sents
    return(sents_corpus)

def clean_sw(sents_corpus, lemmaDict):
    stop = stopwords.words('spanish')
    aux_sents = []
    for sent in sents_corpus:
            aux_sents.append([lemmatize(w, lemmaDict) for w in sent if w not in stop])
            aux_sents[len(aux_sents)-1] = list(filter(None, aux_sents[len(aux_sents)-1])) 
    sents_corpus = aux_sents
    return(sents_corpus)


#Return a list of sentences and a list of words from text
def get_sent_words(text, clean_stopwords):
    pattern = r'''(?ix)    # set flag to allow verbose regexps
     (?:[A-Z]\.)+        # abbreviations, e.g. U.S.A.
   | \w+(?:-\w+)*        # words with optional internal hyphens
   | \$?\d+(?:\.\d+)?%?  # currency and percentages, e.g. $12.40, 82%
   | \.\.\.            # ellipsis
   | [][.,;"'?():-_`]  # these are separate tokens; includes ], [
    '''
    tokenizer = RegexpTokenizer(pattern)
    corpus = PlaintextCorpusReader('.', text, word_tokenizer=tokenizer)
    lemmaDict = load_lemmaDict()
    if not clean_stopwords: 
        sents_corpus = clean_sents_words(corpus.sents(), lemmaDict)
    else:
        sents_corpus = clean_sw(corpus.sents(), lemmaDict)
    return (sents_corpus)
