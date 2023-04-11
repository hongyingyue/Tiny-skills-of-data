from math import log
import pandas as pd
import os
from itertools import chain


#https://stackoverflow.com/questions/8870261/how-to-split-text-without-spaces-into-list-of-words/11642687#11642687
def create_word():
    final_word_list=[]
    word=pd.read_excel('word.xlsx',header=None)
    word_list=list(chain.from_iterable(word.values.tolist()))
    word_list=list(set(word_list))

    for word in word_list:
        final_word_list.append(str(word).split(' '))
    final_word_list=list(chain.from_iterable(final_word_list))+['/','-','(',')']

    file=open('words.txt','w')
    for word in final_word_list:
        file.write(word)
        file.write('\n')
    file.close()


if not os.path.exists('words.txt'):
    create_word()
words = open("words.txt").read().split()
wordcost = dict((k, log((i+1)*log(len(words)))) for i,k in enumerate(words))
maxword = max(len(x) for x in words)


def infer_spaces(s):
    """Uses dynamic programming to infer the location of spaces in a string
    without spaces."""

    # Find the best match for the i first characters, assuming cost has
    # been built for the i-1 first characters.
    # Returns a pair (match_cost, match_length).
    def best_match(i):
        candidates = enumerate(reversed(cost[max(0, i-maxword):i]))
        return min((c + wordcost.get(s[i-k-1:i], 9e999), k+1) for k,c in candidates)

    # Build the cost array.
    cost = [0]
    for i in range(1,len(s)+1):
        c,k = best_match(i)
        cost.append(c)

    # Backtrack to recover the minimal-cost string.
    out = []
    i = len(s)
    while i>0:
        c,k = best_match(i)
        assert c == cost[i]
        out.append(s[i-k:i])
        i -= k

    return " ".join(reversed(out))

