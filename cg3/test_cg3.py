from read_cg3 import read_cg3


def read_one_file(path):
    word_list = []
    test = read_cg3(path)
    # for sentence in test:
    #     word_list.extend(sentence)
    # for w in word_list:
    #     print(w)

read_one_file('../DUO-tagged-testfolder/hum/DUO_BM_0.txt')