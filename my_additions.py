from sickle import Sickle
import os
import errno
import urllib2
import shutil


def print_files(path_to_file):
    with open(path_to_file, 'r') as f:
                for line in f.readlines():
                    print line


def move_file(source, destination):
    shutil.move(source, destination)


def get_x_records(number_of_records):
    """
    Test method for getting a single record
    :return:
    """
    test_file = open('metadata.txt', 'w')
    sickle = Sickle('http://www.duo.uio.no/oai/request')
    records = sickle.ListRecords(metadataPrefix='xoai')
    count = 0
    for record in records:
        count += 1
        for name, metadata in record.metadata.items():
            for i, value in enumerate(metadata):
                if value:
                    print i, value
                    test_file.write(str(i) + ': ' + value.encode('utf8') + '\n')
        if count == number_of_records:
            test_file.close()
            exit()


def create_dir(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise


def delete_file(file_to_delete):
    try:
            os.remove(file_to_delete)
    except OSError, e:
            print ("Error: %s - %s." % (e.filename, e.strerror))


def print_list(l):
    for i, value in enumerate(l):
        print i, value,


def download_pdf(url, path):
        try:
            f = urllib2.urlopen(url)
        except Exception as e:
            print e
            f = None

        if f:
            data = f.read()
            with open(path, "wb") as code:
                code.write(data)
                code.close()