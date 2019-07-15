# JST Transcript Reader

import re
import os

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO


class JSTReader:

    def __init__(self, directory):
        self.dir = directory
        pass

    def convert_pdf_to_txt(self, path):
        rsrcmgr = PDFResourceManager()
        retstr = StringIO()
        codec = 'utf-8'
        laparams = LAParams()
        device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
        fp = open(path, 'rb')
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        password = ""
        maxpages = 0
        caching = True
        pagenos = set()

        for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
            interpreter.process_page(page)

        text = retstr.getvalue()

        fp.close()
        device.close()
        retstr.close()
        return text

    def scan_pdf(self, directory):
        # get the list of files from the current directory
        files = os.listdir(directory)

        # filter the list of files for only pdf files
        files = [fi for fi in files if fi.endswith(".pdf")]

        # for each pdf
        for pdf in files:
            print(pdf)
            a = self.convert_pdf_to_txt(pdf).strip().split("\n")
            if a:
                # for line in a:
                # 	print(line +"\n")

                accepted_courses = set()
                rejected_courses = set()
                b = None
                last_b = b
                for line in a:
                    # print(courses)
                    if line != "Military Experience":
                        if re.match(r'([A-Z]+-[0-9]+-[0-9]+)', line):
                            b = re.findall(r'([A-Z]+-[0-9]+-[0-9]+)', line)
                            last_b = b[0]
                    if line == "Credit Is Not Recommended":
                        # print("No credit: ", last_b)
                        if last_b in accepted_courses:
                            accepted_courses.remove(last_b)
                        rejected_courses.add(last_b)
                    if line == "":
                        continue
                    if line == "Military Experience":
                        break
                    if b is not None:
                        # print("b: ", b)
                        # print("last_b: ", last_b)
                        accepted_courses.add(last_b)
                        b = None

        course_dict = {}
        course_dict['accepted'] = sorted(list(accepted_courses))
        course_dict['rejected'] = sorted(list(rejected_courses))
        return course_dict
