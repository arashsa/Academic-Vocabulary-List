from cg3.read_cg3 import read_cg3 as parser
import os
import multiprocessing as mp
from profilehooks import profile


class CreateWordList():
    """
    Academic Word List 1.0
    This class creates an academic word list given a set of documents.
    """
    @profile
    def __init__(self, path_to_academic_corpus, path_to_regular_corpus):
        self.a_c = self.get_corpus_paths(path_to_academic_corpus, '.txt')  # Paths to academic corpus
        self.r_c = self.get_corpus_paths(path_to_regular_corpus, '.okl')  # Paths to regular corpus

        self.a_c_words = mp.Manager().list()
        self.a_c_counts = mp.Manager().dict()

        self.r_c_words = mp.Manager().list()
        self.r_c_counts = mp.Manager().dict()

        # self.create_lists_and_freqs()
        # print len(self.a_c_words), len(self.a_c_counts)
        # print len(self.r_c_words), len(self.r_c_counts)

    def create_lists_and_freqs(self):
        """
        Starts the processes. Reads files and adds them to list and makes frequency counts.
        :return:
        """
        p1 = mp.Process(target=self.count_words, args=(self.a_c, self.a_c_words, self.a_c_counts))
        p2 = mp.Process(target=self.count_words, args=(self.r_c, self.r_c_words, self.r_c_counts))

        try:
            p1.start()
            p2.start()
        except Exception as e:
            print e

        p1.join()
        p2.join()

    def ratio(self):
        pass

    def range(self):
        pass

    def dispersion(self):
        pass

    def discipline_measure(self):
        pass

    @classmethod
    def get_corpus_paths(cls, path, endswith):
        temp = []
        for root, dirs, files in os.walk(path):
            current_files = []
            for f in files:
                if f.endswith(endswith):
                    current_files.append(os.path.join(root, f))
            if len(current_files) > 0:
                temp.append(current_files)
        return temp

    def count_words(self, paths, l, d):
        """
        appends each word from cg3 parser to l
        :param paths: list of paths
        :param l: list
        :return: None
        """
        processes = []
        for path in paths:
            for f in path:
                # for line in parser(f):
                #     l.extend(line)
                p = mp.Process(target=self.append_and_count, args=(f, l, d))
                try:
                    p.start()
                    processes.append(p)
                except Exception as e:
                    print e
        if processes:
            for proc in processes:
                proc.join()

    @classmethod
    def append_and_count(cls, f, l, d):
        """
        Parses file and appends to list
        :param f: file
        :param l: list
        :return: None
        """
        try:
            for line in parser(f):
                l.extend(line)
                for w in line:
                    if w in d:
                        d[w] += 1
                    else:
                        d[w] = 1
        except Exception as e:
            print e

CreateWordList('DUO-tagged_minim', '/Users/arashsaidi/Work/Corpus/lbk_22.04.14/Unormert/UN02')