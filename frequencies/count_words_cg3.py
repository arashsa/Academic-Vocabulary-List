from os import walk
from cg3.read_cg3 import read_cg3
from profilehooks import profile

@profile()
def count_words():
    corpus_word_list = []
    for (dir_path, dir_names, file_names) in walk('/Users/arashsaidi/Work/Corpus/DUO_Corpus/Bokmaal-tagged-random/'):
        for f in file_names:
            if '.txt' in f:
                current_list = read_cg3(dir_path + f)
                for sentence in current_list:
                    for word in sentence:
                        corpus_word_list.append(word)
    return len(corpus_word_list)

print count_words()