from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from cStringIO import StringIO
import os


def remove_file(path):
    try:
            os.remove(path)
    except OSError, e:
            print ("Error: %s - %s." % (e.filename, e.strerror))


def pdf2text(path):
    string_handling = StringIO()
    try:
        parser = PDFParser(open(path, 'r'))
        save_file = open(path.replace('.pdf', '.txt'), 'w')
        document = PDFDocument(parser)
    except Exception as e:
        print '{} is not a readable document. Exception {}'.format(path, e)
        return

    if document.is_extractable:
        recourse_manager = PDFResourceManager()
        device = TextConverter(recourse_manager,
                               string_handling,
                               codec='utf-8',
                               laparams=LAParams())
        interpreter = PDFPageInterpreter(recourse_manager, device)
        try:
            for page in PDFPage.create_pages(document):
                interpreter.process_page(page)
        except Exception as e:
            print e

        # write to file
        try:
            save_file.write(string_handling.getvalue())
            save_file.close()
        except Exception as e:
            print e

        # deletes pdf
        remove_file(path)

    else:
        print(path, "Warning: could not extract text from pdf file.")
        return