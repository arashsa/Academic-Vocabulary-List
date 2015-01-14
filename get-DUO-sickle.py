from sickle import Sickle
from my_additions import create_dir, download_pdf
from pdf2text import pdf2text
import os
import uuid
import multiprocessing as mp


class GetDuo():
    """
    Class for getting DUO with metadata
    """
    def __init__(self, parallel):
        """
        Init that creates a dictionary with the specs from DUO
        Maps a set of numbers to faculty/institute
        :return: None
        """
        self.spec_list = {}
        with open('specs.txt', 'r') as f:
            p_line = {}
            for line in f:
                if line.split()[0] == 'setName':
                    # a hack to map codes to names of faculty/institute
                    self.spec_list[p_line.split()[1]] = line[8:].rstrip()
                p_line = line
        self.files_to_download_parallel = parallel

        self.cleanup_jobs = []

    def download_multiples(self, process_data):
        """
        Downloads multiple files. First downloads the pdf in parallel, then converts them to txt
        :param process_data:
        :return:
        """
        # Starts downloading pdf
        jobs = []
        for i in process_data:
            p = mp.Process(target=download_pdf, args=(i[0], i[1]))
            jobs.append(p)
            try:
                p.start()
            except Exception as e:
                print e

        # converts pdf to txt after each pdf has been downloaded
        for i, data in enumerate(process_data):
            # print 'converting {}'.format(data[1])
            p = mp.Process(target=pdf2text, args=(data[1],))
            self.cleanup_jobs.append(p)
            jobs[i].join()
            try:
                p.start()
            except Exception as e:
                print e

        # makes sure conversion is finished before starting a new batch
        for job in self.cleanup_jobs:
            job.join()
        print 'Cleaned up jobs for set of {} items...'.format(self.files_to_download_parallel)
        self.cleanup_jobs = []

    def write_record_to_file(self, records, path_to_institute):
        """
        Writes each record in a set of records to file, storing metadata
        :param records:
        :param path_to_institute:
        :return: None
        """
        process_data = []
        for record in records:
            record_data = []  # data is stored in record_data
            for name, metadata in record.metadata.items():

                for i, value in enumerate(metadata):
                    if value:
                        # print value
                        record_data.append(value)
            fulltext = ''
            file_path = ''
            file_path_metadata = ''
            unique_id = str(uuid.uuid4())
            get_file = True
            for data in record_data:
                if 'Fulltext' in data:
                        # the link to the pdf
                    fulltext = data.replace('Fulltext ', '')
                    # path where the txt file will be stored
                    file_path = '/' + os.path.basename(data).replace('.pdf', '') + unique_id + '.pdf'
                    # path where the metadata will be stored
                    file_path_metadata = '/' + os.path.basename(data).replace('.pdf', '') + unique_id + '_metadata.txt'
                    # print fulltext, file_path
                if 'embargoedaccess' in data:
                    get_file = False

            # Write metadata to file
            if fulltext and get_file:
                try:
                    write_metadata = open(path_to_institute + file_path_metadata, 'w')
                    for i, data in enumerate(record_data):
                        write_metadata.write('MD_' + str(i) + ': ' + data.encode('utf8') + '\n')
                    write_metadata.close()
                except Exception as e:
                    # Exceptions due to missing path to file
                    print 'Exception when writing metadata: {}'.format(e)
                    print fulltext, path_to_institute, file_path_metadata

                process_data.append((fulltext, path_to_institute + file_path))

            # number of downloads at a time
            if len(process_data) == self.files_to_download_parallel:
                self.download_multiples(process_data)
                process_data = []

        # cleanup
        if process_data:
            print 'Cleaning up...'
            self.download_multiples(process_data)

    def get_records(self, faculty='#########'):
        """
        Starts the process of retrieving DUO files
        :return: None
        """
        # gets sickle from OAI
        sickle = Sickle('http://www.duo.uio.no/oai/request')
        sets = sickle.ListSets()  # gets all sets
        main_path = ''
        for recs in sets:
            for rec in recs:
                if rec[0] == 'setSpec' and rec[1][0] in self.spec_list.keys():
                    print self.spec_list[rec[1][0]]
                    if faculty not in self.spec_list[rec[1][0]]:
                        path_to_institute = 'DUO/'+main_path+'/'+self.spec_list[rec[1][0]]  # path to institute
                        create_dir(path_to_institute)
                        try:
                            # gets record and writes to file
                            records = sickle.ListRecords(metadataPrefix='xoai', set=rec[1][0], ignore_deleted=True)
                            self.write_record_to_file(records, path_to_institute)
                        except Exception as e:
                            print e
                    else:
                        # creates head directory
                        main_path = self.spec_list[rec[1][0]]
                        create_dir('DUO/'+main_path)

# Number is for how many files to download at the same time
test = GetDuo(20)
test.get_records()