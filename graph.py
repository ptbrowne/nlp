import pickle, networkx as nx
from copy import copy
from collections import defaultdict

with open("l2.pickle") as f:
    lyrics = pickle.load(f)
    

def divide_lyrics(lyric):
    for t in lyric["tags"]:
        l = copy(lyric)
        l["tags"] = t
        yield l

lyrics = (l for l in lyrics if l.get("title"))
lyrics = (dl for l in lyrics for dl in divide_lyrics(l))

g = nx.DiGraph()

counts = defaultdict(lambda : defaultdict(float))

for l in lyrics:
    if l.get("genre"):
        for genre in l["genre"]:
            counts[genre][l["tags"]] += 1

for genre in counts:
    print genre
    for tag in counts[genre]:
        g.add_node(genre, t = "genre")
        g.add_node(tag, t = "tag")
        g.add_edge(genre, tag, weight =  counts[genre][tag])
        
with open("bob.gexf", "w") as f:
    nx.write_gexf(g, f)
 
