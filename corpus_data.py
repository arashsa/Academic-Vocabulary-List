#!/usr/bin/python
#  -*- coding: utf8 -*-

import os
data = open('DUO_data/corpus_data.txt', 'w')


def write_to_data(words, articles, faculty):
    data.write('\n{}: {} articles {} words'.format(faculty, articles, words))


def count(path):
    words = 0
    articles = 0
    for root, dirs, files in os.walk(path):
        print 'reading: ' + root
        for f in files:
            if f.endswith('.obt'):
                articles += 1
                p = os.path.join(root, f)
                with open(p) as duo_file:
                        for line in duo_file.readlines():
                            words += len(line.split())
    write_to_data(words, articles, path)


def gather_obt_data(path):
    for root, dirs, files in os.walk(path, topdown=False):
        for d in dirs:
            _path = os.path.join(root, d)
            count(_path)

gather_obt_data('/Users/arashsaidi/PycharmProjects/DUO/DUO_new_BB/')
# count('/Users/arashsaidi/PycharmProjects/DUO/DUO_new_BB')