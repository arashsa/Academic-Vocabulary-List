import os
import sys


def remove_pdf(path):
    """
    Removes all pdf, the failed txt conversion, and metadata
    :param path: root path
    :return:
    """
    files_to_remove = []
    for root, dirs, files in os.walk(path):
        for f in files:
            if f.endswith('.pdf'):
                pdf = os.path.join(root, f)
                meta = pdf.replace('.pdf', '_metadata.txt')
                files_to_remove.append(pdf)
                files_to_remove.append(meta)
                os.remove(pdf)
                os.remove(meta)


def count_words(path):
    """
    :param path:
    :return:
    """
    data = open('DUO-data.txt', 'w')
    count = 0
    words = 0
    for root, dirs, files in os.walk(path):
        for f in files:
            if not f.endswith('_metadata.txt') and f.endswith('.txt'):
                count += 1
                file_name = os.path.join(root, f)
                with open(file_name) as duo_file:
                    for line in duo_file.readlines():
                        words += len(line.split())
                        print line.split()
    data.write('DUO-Corpus:\n Files: {}\n Words: {}'.format(count, words))

if __name__ == '__main__':
    remove_pdf(sys.argv[1])