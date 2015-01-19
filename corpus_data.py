#!/usr/bin/python
#  -*- coding: utf8 -*-

import os
current_faculty = 'Det utdanningsvitenskapelige fakultet/'
current_path = 'Institutt for spesialpedagogikk'

data = open('DUO_data/corpus_data.txt', 'a')


def gather_data(path):
    words = 0
    articles = 0
    for root, dirs, files in os.walk(path):
        for f in files:
            if not f.endswith('_metadata.txt') and f.endswith('.txt'):
                articles += 1
                p = os.path.join(root, f)
                with open(p) as duo_file:
                        for line in duo_file.readlines():
                            words += len(line.split())
    write_to_data(words, articles, current_path)


def write_to_data(words, articles, faculty):
    data.write('\n{}: {} articles {} words'.format(faculty, articles, words))
    data.close()


def gather_obt_data(path):
    for root, dirs, files in os.walk(path):
        for f in files:
            if f.endswith('txt.obt'):
                print f
