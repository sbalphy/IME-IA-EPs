from nltk.util import ngrams
from collections import Counter


def get_empty_counter():
    """Returns an empty Counter"""
    return Counter()

def generate_n_grams(text, N):
    """Returns the list of N-grams from text"""
    n_grams =  ngrams(text.split(), N)
    n_grams = [grams for grams in n_grams]
    return n_grams


def FindPath(predecessor, source, target):
    'Backtracks edges from target until souce, using `predecessor` list'
    path = Stack()
    u = target
    while u != source:
        u,a = predecessor[u]
        path.put((u,a))
    while not path.empty():
        yield path.get()        

class Stack:
    'Implements an array-based Stack'
    def __init__(self, items=()):
        self._items = [] # empty
    def put(self, item): # add to top
        self._items.append(item)
    def get(self):       # get from top
        return self._items.pop()
    def top(self):       # peek top
        return self._items[-1]
    def empty(self):
        return len(self._items) == 0

def read_documents(options):
    """
    Returns the text from the given documents or the combination of them all.
    """
    if options == "safatle":
        return open("Limposafatle.txt", encoding='utf-8').read()
    elif options == "machado":
        return open("Limpomachado.txt", encoding='utf-8').read()
    elif options == "mmorpho":
            return open("Limpommorpho.txt", encoding='utf-8').read()
    elif options == "flor":
            return open("Limpoflor.txt", encoding='utf-8').read()
    elif options == "saka":
            return open("Limposaka.txt", encoding='utf-8').read()
    elif options == "all":
        return open("Limpommorpho.txt", encoding='utf-8').read() + open("Limpoflor.txt", encoding='utf-8').read() + open("Limpomachado.txt", encoding='utf-8').read() + open("Limposaka.txt", encoding='utf-8').read() + open("Limposafatle.txt", encoding='utf-8').read()
    else:
        return open("Limposafatle.txt", encoding='utf-8').read()
    
def print_search_result(S):
    if S is None:
        print("Search failed, could not reach the goal")
    else:
        S = list(S)
        print("The solution has", len(S), "steps")
        for (s,a) in S:
            print(s)