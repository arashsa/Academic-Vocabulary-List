#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# import re
import os
#
# path = '/Users/arashsaidi/PycharmProjects/DUO/DUO_new_BB/Det teologiske fakultet/Kristendomsstudier copy'
# for root, dirs, files in os.walk(path):
#     for f in files:
#         if not f.endswith('_metadata.txt'):
#             path = os.path.join(root, f)
#             with open(path, 'r') as current_file:
#                 test = current_file.read()
#                 rx = re.compile('/[^(\\x20-\\x7F\\n)]+/u')
#                 res = rx.sub(' ', test).strip()
#                 write = open(path, 'w')
#                 write.write(test)


def is_num(word):
    try:
        float(word)
        return True
    except ValueError:
        return False


def cleanup(path):
    extra = open(path + '/extra.txt', 'w')
    for root, dirs, files in os.walk(path):
        for f in files:
            if f.endswith('.txt') and not f.endswith('_metadata.txt'):
                p = os.path.join(root, f)
                cleaned = open(p.replace('.txt', '_cleaned.txt'), 'w')
                with open(p, 'r') as current_file:
                    for line in current_file.readlines():
                        l = line.split()
                        if l:
                            for w in l:
                                if len(w) < 30 and not is_num(w):
                                    cleaned.write(w + ' ')
                                else:
                                    extra.write(w + '\n')
                            cleaned.write('\n')

cleanup('DUO_new_BB')
# length = 0
# word = ''
# with open('duo_list_alpha.txt') as f:
#     for line in f.readlines():
#         if len(line) > 0:
#             try:
#                 if len(line.split()[0]) > length:
#                     length = len(line.split()[0])
#                     word = line.split()[0]
#             except IndexError:
#                 print line
# print length
# print word