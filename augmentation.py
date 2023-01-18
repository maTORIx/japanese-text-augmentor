import shutil
import sqlite3
import os
import gzip
import sys
import readline
import random
import MeCab
import numpy as np
import itertools
from vec import calc_text_distances, sort_with_distance

dbfile = "wnjpn.db"

def setup():
    if os.path.exists(dbfile):
        return
    elif not os.path.exists(dbfile + ".gz"):
        os.system("wget https://github.com/bond-lab/wnja/releases/download/v1.1/wnjpn.db.gz")
    with gzip.open('wnjpn.db.gz', 'rb') as f_in:
        with open('wnjpn.db', 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

def get_synonyms(word):
    conn = sqlite3.connect(dbfile)
    cur = conn.cursor()
    result = cur.execute("""
    SELECT lemma FROM word
    WHERE wordid IN (                                                                                                           SELECT wordid FROM sense
        WHERE synset IN (
            SELECT synset FROM sense
            WHERE wordid IN (
                SELECT wordid FROM word WHERE lemma = ?
            )
        )
    ) AND lang = "jpn" AND lemma != ?;
    """, (word,word))
    return [i[0] for i in result.fetchall()]

def isChangeable(surface, feature):
    if len(surface) <= 1:
        return False
    elif feature.startswith("動詞"):
        return True
    elif feature.startswith("名詞"):
        return True
    return False

def generateCombinations(selectable_words, max_n, max=1000):
    result = []
    selectable_idx_list = []
    for idx, selectable in enumerate(selectable_words):
        if len(selectable) > 1:
            selectable_idx_list.append(idx)
            
    n = max_n
    if len(selectable_idx_list) < max_n:
        n = len(selectable_idx_list)

    for word_combination in itertools.combinations(selectable_idx_list, n):
        selectable_words_idx_list = [list(range(len(selectable_words[i])))[1:] for i in word_combination]
        for combination in itertools.product(*selectable_words_idx_list):
            tmp = [0 for i in range(len(selectable_words))]
            for idx, i in enumerate(combination):
                tmp[word_combination[idx]] = i
            result.append(tmp)

            if len(result) > max:
                return result
    return result
                    

def augmentation(text, n_max, gen_max, combination_max=1000000):
    tagger = MeCab.Tagger()
    node = tagger.parseToNode(text)
    words = []
    selectable_words = []
    while node:
        words.append([node.surface, node.feature])
        node = node.next
    for word in words:
        if not isChangeable(word[0], word[1]):
            selectable_words.append([word[0]])
        else:
            synonyms = get_synonyms(word[0])
            synonyms.append(word[0])
            selectable_words.append(synonyms)

    n1combs = np.array(generateCombinations(selectable_words, 1, combination_max))
    n1combs_texts = []
    for combination in n1combs:
        n1combs_texts.append("".join([selectable_words[wi][si] for wi, si in enumerate(combination)]))
    word_distances = np.array(calc_text_distances(text, n1combs_texts)).reshape(len(n1combs),1)

    combinations = generateCombinations(selectable_words, n_max, combination_max)
    inspected_combination_distances = np.zeros((len(combinations),))
    for idx, combination in enumerate(combinations):
        tmp = np.array(combination)
        tmp[tmp == 0] = -1
        inspected = np.sum((tmp == n1combs) * word_distances)
        inspected_combination_distances[idx] = inspected
    ranked_combinations = map(lambda x:combinations[x[0]], sorted(enumerate(inspected_combination_distances), key=lambda x:x[1]))

    size = gen_max
    if len(combinations) < gen_max:
        size = len(combinations)

    result = []
    for combination in list(ranked_combinations)[:size]:
        result.append("".join([selectable_words[wi][si] for wi, si in enumerate(combination)]))
    return result
        
if __name__ == "__main__":
    setup()
    gen_max = int(sys.argv[1])
    n_max = int(sys.argv[2])
    original = sys.argv[3]
    for i in sort_with_distance(original, augmentation(original, n_max, gen_max)):
        print(i)

    
