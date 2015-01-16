import os


def remove_file(path):
    try:
        os.remove(path)
    except Exception as e:
        print e


def remove_pdf_and_empty_files(path):
    """
    Removes all pdf, the failed txt conversion, and metadata
    :param path: root path
    :return:
    """
    count = 0
    for root, dirs, files in os.walk(path):
        for f in files:
            count += 1
            if f.endswith('.pdf'):
                pdf = os.path.join(root, f)
                meta = pdf.replace('.pdf', '_metadata.txt')
                text = pdf.replace('.pdf', '.txt')
                if os.path.isfile(pdf):
                    remove_file(pdf)
                if os.path.isfile(meta):
                    remove_file(meta)
                if os.path.isfile(text):
                    remove_file(pdf)
    print count


def cleanup(path):
    for root, dirs, files in os.walk(path):
        for f in files:
            path = os.path.join(root, f)
            if os.path.getsize(path) == 0:
                meta = path.replace('.txt', '_metadata.txt')
                if os.path.isfile(path):
                    remove_file(path)  # removes text
                if os.path.isfile(meta):
                    remove_file(meta)  # removes meta


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
                        # print line.split()
    data.write('DUO-Corpus:\n Files: {}\n Words: {}'.format(count, words))

# remove_pdf_and_empty_files('DUO')
count_words('DUO_new_BB')
# cleanup('DUO')