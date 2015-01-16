# !/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import shutil
import errno


def create_dir(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise


class Detection():
    """A simple method for detecting English, Norwegian (bokmaal and nynorsk).
    The method simply counts words
    """
    def __init__(self, path):
        """
        :param path: Path where all files to be changed
        :return:
        """
        # list from http://omilia.uio.no/frekvenser/index.php
        # bokmaal freq list
        # 'vi', 'vil', 'så', 'skal', 'også', 'etter', 'ble', 'ved', 'dette'
        self.bm = ['en', 'de', 'ikke', 'et', 'fra', 'kan', 'jeg', 'seg']

        # list from http://omilia.uio.no/frekvenser/index.php
        # nyorsk freq list
        self.nn = ['ikkje', 'dei', 'ein', 'ho', 'eg', 'eit', 'frå', 'berre']

        # list from http://www.wordfrequency.info/top5000.asp
        # english freq list
        # 'that', 'you', 'he', 'with', 'on', 'do', 'say', 'this', 'they', 'but', 'we', 'his', 'from', 'that', 'not',
        # 'by', 'she', 'or', 'as', 'what'
        self.en = ['the', 'be', 'and', 'of', 'in', 'to', 'have', 'it']

        self.word_count_en_bm_nn = {'en': 0, 'bm': 0, 'nn': 0}

        self.en_count = 0
        self.bm_count = 0
        self.nn_count = 0
        self.corrupt_count = 0
        self.all_count = 0

        self.info = open('DUO_info.txt', 'w')

        self.path = path

        # start reading files
        self.read_files()
        self.write_info()

    def read_files(self):
        """ Recursively traverses all files in the path
        :return: None
        """
        for root, dirs, files in os.walk(self.path):
            # Goes through files and sends them to check_language
            # Deletes pdf files
            for f in files:
                if not f.endswith('_metadata.txt') and f.endswith('.txt'):
                    current_path_to_file = os.path.join(root, f)
                    current_file = open(current_path_to_file, 'r')
                    self.check_language(current_file, current_path_to_file, root)

    def check_language(self, text_file, path_to_file, root):
        """ Checks words in file for occurrences in lists
        :param text_file: The current text_file
        :return: None
        """
        for line in text_file.readlines():
            for word in line.split():
                lower_case = word.lower()
                if lower_case in self.bm:
                    self.word_count_en_bm_nn['bm'] += 1
                elif lower_case in self.nn:
                    self.word_count_en_bm_nn['nn'] += 1
                elif lower_case in self.en:
                    self.word_count_en_bm_nn['en'] += 1

        self.move_file(path_to_file, root)

    def move_file(self, path_to_file, root):
        """
        If file is not norwegian_bokmaal file is moved to a different location
        :param path_to_file: Path to the file to be moved
        :return:
        """
        meta = path_to_file.replace('.txt', '_metadata.txt')
        key = max(self.word_count_en_bm_nn, key=self.word_count_en_bm_nn.get)
        # print "largest {}\n".format(key)

        if self.word_count_en_bm_nn[key] < 50:
            self.corrupt_count += 1
            create_dir('DUO-Corrupted/' + root)
            if os.path.isfile(path_to_file):
                shutil.move(path_to_file, 'DUO-Corrupted/' + path_to_file)
            if os.path.isfile(meta):
                shutil.move(meta, 'DUO-Corrupted/' + meta)
        elif key == 'nn':
            self.nn_count += 1
            create_dir('DUO-NN/' + root)
            if os.path.isfile(path_to_file):
                shutil.move(path_to_file, 'DUO-NN/' + path_to_file)
            if os.path.isfile(meta):
                shutil.move(meta, 'DUO-NN/' + meta)
        elif key == 'en':
            self.en_count += 1
            create_dir('DUO-English/' + root)
            if os.path.isfile(path_to_file):
                shutil.move(path_to_file, 'DUO-English/' + path_to_file)
            if os.path.isfile(meta):
                shutil.move(meta, 'DUO-English/' + meta)

        self.word_count_en_bm_nn['bm'] = 0
        self.word_count_en_bm_nn['nn'] = 0
        self.word_count_en_bm_nn['en'] = 0
        self.all_count += 1

    def write_info(self):
        self.info.write("-" * 30+'\n')
        self.info.write("DUO corpus:"+'\n')
        self.info.write("All articles: {}\n".format(self.all_count))
        self.info.write("English articles: {}\nBM articles: {}\nNN articles: {}\nCorrupt articles: {}'\n'".format(
            self.en_count, self.bm_count, self.nn_count, self.corrupt_count))
        self.info.write("-" * 30)

Detection('DUO')