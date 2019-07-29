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
        self.tdir = self.idir + 'text/'  # text file directory
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

        os.system('mkdir ' + self.idir)
        index = 0
        for image in images:
            image.save(self.idir + "image-" + str(index) + ".jpg")
            index += 1

    # old conversion function
    # def convert_to_image(self, file):
    #     # Convert the jst file (presumably PDF) into an image (jpg) using imagemagick
    #     # Command for imagemagick version 6 is "convert-im6 inputfile -density (value) outputfile"
    #     # Higher density for higher quality, up to a certain point. Will take longer to run at higher values of course
    #     os.system('mkdir ' + self.idir)
    #     os.system('(cd ' + self.idir + '; convert-im6 -density 300 ../"' + file + '" image' + '.jpg' + ')')

    def convert_to_text(self, file):
        # convert newly generated image files to text files using pytesseract
        end = len(file) - 4
        filename = file[0:end] + '.txt'
        filestring = pytesseract.image_to_string((Image.open(file)))
        outputfile = open(filename, 'w')
        outputfile.write(filestring)
        outputfile.close()

    def scan_image(self):
        # scan images following conversion from pdf
        accepted_courses = set()
        rejected_courses = set()
        # file_list = []
        image_glob = self.idir + '*.jpg'
        image_list = glob.glob(image_glob)
        image_list.sort()

        os.system('mkdir ' + self.tdir)

        pool = mp.Pool(mp.cpu_count())

        pool.map(self.convert_to_text, [fn for fn in image_list])

        file_list = glob.glob(self.idir + '*.txt')
        file_list.sort()

        flag = True
        # temp = None
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
                        if re.search(r'((MC|NV)-[0-9]+-[0-9]+)', line):
                            temp = re.findall(r'((MC|NV)-[0-9]+-[0-9]+)', line)
                            add = temp[0][0]
                    if add is not None:
                        accepted_courses.add(add)
                        prev = add
                        add = None
                    if "Credit Is Not Recommended" in line:
                        if prev is not None:
                            if prev in accepted_courses:
                                accepted_courses.remove(prev)
                            rejected_courses.add(prev)
                            prev = None
        return accepted_courses, rejected_courses

    def convert_pdf_to_txt(self, path):
        # read text-based pdf
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
        start_time = time.time()
        # get the list of files from the current directory
        files = os.listdir(self.dir)

        # filter the list of files for only pdf files
        files = [fi for fi in files if fi.endswith(".pdf")]

        # for each pdf
        for pdf in files:
            a = self.convert_pdf_to_txt(self.dir + pdf).strip().split("\n")
            if len(a[0]) > 0:
                # print('----------------------------text-based PDF, running as normal--------------------')

                accepted_courses = set()
                rejected_courses = set()
                b = None
                last_b = b
                flag = True
                if flag:
                    for line in a:
                        # the inside of this loop is used twice - could put in a function somewhere somehow
                        if line == "Military Experience" or line == "Other Learning Experiences":
                            flag = False
                            break
                        if line == "":
                            continue
                        if line != "Military Experience":
                            if re.match(r'([A-Z]+-[0-9]+-[0-9]+)', line):
                                b = re.findall(r'([A-Z]+-[0-9]+-[0-9]+)', line)
                                last_b = b[0]
                        if "Credit Is Not Recommended" in line:
                            if last_b in accepted_courses:
                                accepted_courses.remove(last_b)
                            rejected_courses.add(last_b)
                        if b is not None:
                            accepted_courses.add(last_b)
                            b = None

                course_dict = {}
                course_dict['accepted'] = sorted(list(accepted_courses))
                course_dict['rejected'] = sorted(list(rejected_courses))
            else:  # OCR route
                print('------------------image-based PDF, running conversion------------------------')
                conv_start = time.time()
                self.convert_to_image(pdf)
                conv_end = time.time()
                conv_time = conv_end - conv_start
                print('------------- Conversion finished, run time: ', conv_time, '------------------')
                accepted_courses, rejected_courses = self.scan_image()
                course_dict = {}
                course_dict['accepted'] = sorted(list(accepted_courses))
                course_dict['rejected'] = sorted(list(rejected_courses))

        end_time = time.time()
        runtime = end_time - start_time
        print('-------------------------------- total run time: ', runtime, '---------------------------------')
        return course_dict

