import os

def bigrams_freq(path='/home/anya/python/web/app/ria'):
    bigramsFreq = {}
    for root, dirs, files in os.walk(path):
        for file in files:
            fileName = os.path.join(root, file)
            with open(fileName, encoding='utf-8') as f:
                words = []
                bigrams = []
                for sent in f:
                    words += sent.strip('\n').lower().split()
                for i in range(len(words)-1):
                    bigrams.append(' '.join(words[i:i+2]))
                for bigram in bigrams:
                    if bigram in bigramsFreq:
                        bigramsFreq[bigram] += 1
                    else:
                        bigramsFreq[bigram] = 1
    return bigramsFreq

def word_bigram(word):
    bigramList = []
    wordBigram = {}
    bigramsFreq = bigrams_freq()
    for key in bigramsFreq:
        if word in key.split():
            wordBigram[key] = bigramsFreq[key]
    inverse = [(v, k) for k, v in wordBigram.items()]
    bigramList = [(i[1], i[0]) for i in sorted(inverse, reverse=True)[:10]]
    return bigramList