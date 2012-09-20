import pickle, nltk
from stopwords import stopwords, is_stopword
from nltk import TextCollection, Text
from pprint import pprint
from copy import copy
import time
from nltk.corpus import brown

with open("l2.pickle") as f:
    lyrics = pickle.load(f)

tags = ["love", "motivation",  "sadness"]
print tags 
with open("/usr/share/dict/american-english") as dico:
    dict_words = list(dico.readlines())

def valid(tag):
    return tag and (tag.startswith("VB") or tag.startswith("JJ"))

def all_words(lyrics):
    for l in lyrics:
        for w in nltk.word_tokenize(" ".join(l["lyrics"])):
#             print w, unigram_tagger.tag([w])
             if l.get("title") and (not is_stopword(w)) and valid(unigram_tagger.tag([w])[0][1]):
                yield w.lower()

def document_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
    return features


def divide_lyrics(lyric):
    for t in lyric["tags"]:
        if t in tags:
            l = copy(lyric)
            l["tags"] = t
            yield l

brown_tagged_sents = brown.tagged_sents(categories='news')
brown_sents = brown.sents(categories='news')
unigram_tagger = nltk.UnigramTagger(brown_tagged_sents)
unigram_tagger.tag(brown_sents[2007])

lyrics = [l for l in lyrics if l.get("title")]
aw = nltk.FreqDist(all_words(lyrics))
word_features = sorted(aw.keys())
#all_words = nltk.FreqDist(w.lower() for l in lyrics for w in nltk.word_tokenize(" ".join(l["lyrics"])) if l.get("title") if not is_stopword(w))
#word_features = sorted(all_words.keys())

print word_features
lyrics = [dl for l in lyrics for dl in divide_lyrics(l)]

t = time.time()
featuresets = [(document_features(l["lyrics"]), l["tags"]) for l in lyrics]
train_set, test_set = featuresets[100:], featuresets[:100]
classifier = nltk.NaiveBayesClassifier.train(train_set)

#print document_features(lyrics[1]["lyrics"])
print time.time() - t
print nltk.classify.accuracy(classifier, test_set)

classifier.show_most_informative_features(100)

