# JST Transcript Reader

import re
import os
import pytesseract
from PIL import Image
import glob
import multiprocessing as mp
import time
from pdf2image import convert_from_path, convert_from_bytes
from pdf2image.exceptions import PDFSyntaxError, PDFPageCountError, PDFInfoNotInstalledError

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO


class JSTReader:

    def __init__(self, directory):
        self.dir = directory  # base directory, where JST is uploaded/stored
        self.idir = self.dir + 'images/'  # image directory
        pass

    def clear_dir(self, mkdir):
        # Empty the working directory
        # Currently done by deleting then (if desired) making it again
        os.system('rm -rf ' + self.dir)
        if mkdir:
            os.system('mkdir ' + self.dir)

    def convert_to_image(self, file):
        # new conversion function using pdf2image
        filedir = self.dir + file
        # dpi=300 seems to be the sweet spot
        # using mp.cpu_count() for thread count allows us to multithread without using too many threads
        images = convert_from_path(filedir, dpi=300, thread_count=mp.cpu_count())

        index = 0
        for image in images:
            image.save(self.idir + "image-" + str(index) + ".jpg")
            index += 1

    def convert_to_text(self, file):
        # convert newly generated image files to text files using pytesseract
        end = len(file) - 4
        filename = file[0:end] + '.txt'
        filestring = pytesseract.image_to_string((Image.open(file)))
        outputfile = open(filename, 'w')
        outputfile.write(filestring)
        outputfile.close()

    def scan_file(self, image_based):
        # scan files for course codes
        # uses regex to search text files
        # uses multiprocessing where possible
        accepted_courses = set()
        rejected_courses = set()

        # if pdf was image-based, grab a list of images from the image directory
        if image_based:
            image_glob = self.idir + '*.jpg'
            image_list = glob.glob(image_glob)
            image_list.sort()

            pool = mp.Pool(mp.cpu_count())

            pool.map(self.convert_to_text, [fn for fn in image_list])

        file_list = glob.glob(self.idir + '*.txt')
        # print("-----------------list of text files-----------------------")
        # print(file_list)
        # print(os.system('ls ' + self.idir))
        file_list.sort()

        flag = True
        add = None
        prev = None
        for filename in file_list:
            if flag:
                for line in open(filename):
                    if "Military Experience" in line or "Other Learning Experiences" in line:
                        flag = False
                        break
                    if line == "":
                        continue
                    if line != "Military Experience":
                        if re.search(r'((MC|NV|AR|CG|DD)(-|—)[0-9\s]+-[0-9\s]+)', line):
                            temp = re.findall(r'((MC|NV|AR|CG|DD)(-|—)[0-9\s]+-[0-9\s]+)', line)
                            # print('---------------------------regex result--------------------')
                            # print(temp)
                            add = temp[0][0]
                            add = add.replace(" ", "")
                            add = add.replace("—", "-")
                            # print('-----------------------course found: -------------------------')
                            # print(add)
                    if add is not None:
                        accepted_courses.add(add)
                        prev = add
                        add = None
                    if "Credit Is Not Recommended" in line:
                        # print('-------------------------line-----------------------')
                        # print(line)
                        # print(prev)
                        # print(accepted_courses)
                        if prev is not None:
                            if prev in accepted_courses:
                                accepted_courses.remove(prev)
                            rejected_courses.add(prev)
                            prev = None
                        # print(accepted_courses)
        return accepted_courses, rejected_courses

    def convert_pdf_to_txt(self, path):
        # convert text-based pdf to text file
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

    def scan_pdf(self):
        accepted_courses = set()
        rejected_courses = set()
        start_time = time.time()
        # get the list of files from the current directory
        files = os.listdir(self.dir)

        # filter the list of files for only pdf files
        files = [fi for fi in files if fi.endswith(".pdf")]

        os.system('mkdir ' + self.idir)
        # print('----------------------------idir has been created---------------------')
        # print(os.getcwd())

        # for each pdf
        for pdf in files:
            filestring = self.convert_pdf_to_txt(self.dir + pdf).strip().split("\n")
            # print('---------------------------filestring--------------------------------')
            # print(filestring)
            if len(filestring[0]) > 0:
                owd = os.getcwd()
                os.chdir(self.idir)
                with open('jst.txt', 'w') as outfile:
                    for item in filestring:
                        outfile.write("%s\n" % item)
                os.chdir(owd)

                accepted_courses, rejected_courses = self.scan_file(False)

            else:  # OCR route
                print('------------------image-based PDF, running conversion------------------------')
                conv_start = time.time()
                self.convert_to_image(pdf)
                conv_end = time.time()
                conv_time = conv_end - conv_start
                print('------------- Conversion finished, run time: ', conv_time, '------------------')
                accepted_courses, rejected_courses = self.scan_file(True)

        course_dict = {}
        course_dict['accepted'] = sorted(list(accepted_courses))
        course_dict['rejected'] = sorted(list(rejected_courses))
        end_time = time.time()
        runtime = end_time - start_time
        print('-------------------------------- total run time: ', runtime, '---------------------------------')
        return course_dict
