import pickle, nltk
from stopwords import stopwords, is_stopword
from nltk import TextCollection, Text
from pprint import pprint
from nltk.corpus import brown

brown_tagged_sents = brown.tagged_sents(categories='news')
brown_sents = brown.sents(categories='news')
unigram_tagger = nltk.UnigramTagger(brown_tagged_sents)

def valid(word):
    tag = unigram_tagger.tag([word])[0][1]
    return tag and tag.startswith("NN")

with open("l2.pickle") as f:
    lyrics = pickle.load(f)

i = 0
def add_info(lyric, text_col, i=0):

    def prep_word(w):
        return w.lower()
    
    a = dict(lyric)
    a["lyrics"] = Text(w.lower() for w in nltk.word_tokenize(" ".join(a["lyrics"]).encode("utf-8")))
    a["terms"] = set(w for w in a["lyrics"] if not is_stopword(w) and valid(w))
    
    a["tf_idf"] = dict(sorted( ( (t, text_col.tf_idf(t, a["lyrics"])) for t in a["terms"] ), key=lambda x : x[1]) )
    i += 1
    print i
    return a
    
ts = TextCollection([Text((w.lower() 
                                for w in nltk.word_tokenize(" ".join(l["lyrics"]).encode('utf-8')) if not is_stopword(w) and valid(w) ) , 
                         name = l["id"]) 
                    for l in lyrics if l.get("id")])

#lyrics = map(lambda x : add_info(x[1], ts, x[0]), ((i, l) for i, l in enumerate(lyrics) if l.get("id")))

#with open("withtfidf.pickle", "w") as f:
#    pickle.dump(lyrics, f)

with open("withtfidf.pickle", "r") as f:
    lyrics = pickle.load(f)
    
lyrics = dict((l["id"], l) for l in lyrics)

def similar_lyrics(lyric):
    for l in lyrics.values():
        if l["lyrics"] != lyric["lyrics"]:
                total_terms = lyric["terms"].union(l["terms"])
                a, b = [lyric["tf_idf"].get(t) or 0 for t in total_terms], [l["tf_idf"].get(t) or 0 for t in total_terms]
                yield nltk.cosine_distance(a, b), l["id"]

def give_me_similar(id):
    p, s_id = min(sorted(list(similar_lyrics(lyrics[id]))))
    return lyrics[s_id]["title"], p, s_id

def print_l(id):
    print " ".join(lyrics[id]["lyrics"])

def most_similar(id):
    return min(give_me_similar(id))
    
for v in lyrics.values()[:10]:
    print v["id"], v["lyrics"]



