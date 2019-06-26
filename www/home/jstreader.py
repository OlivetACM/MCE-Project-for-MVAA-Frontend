import os
import re


def clear_dir(work_dir, mkdir):
    # Empty the working directory
    # Currently done by deleting then (if desired) making it again
    os.system('rm -rf ' + work_dir)
    if mkdir:
        os.system('mkdir ' + work_dir)


def copy_file(trans_dir, work_dir, file):
    # Copy the jst file into the working directory
    os.system('cp ' + trans_dir + file + ' ' + work_dir)


def convert_to_image(img_dir, file):
    # Convert the jst file (presumably PDF) into an image (jpg) using imagemagick
    # Command for imagemagick version 6 is "convert-im6 inputfile -density (value) outputfile"
    # Higher density for higher quality, up to a certain point. Will take longer to run at higher values of course
    os.system('mkdir ' + img_dir)
    os.system('(cd ' + img_dir + '; convert-im6 -density 200 ../' + file + ' image' + '.jpg' + ')')


def find_number(numstring):
    newstring = ''
    for char in numstring:
        if char is 'l':
            newstring += '1'
        elif char is 's' or char is 'S':
            newstring += '5'
        else:
            newstring += char
    return newstring


def reorder_files(file_list, trans_dir):
    # Use regular expressions to correctly read the page number,
    # then reorder the pages from 0 to n, skipping pages with
    # irrelevant info, such as the summary page
    # regex = r"(Page|page)\s*([sSl]|\d)*\s*of\s*([sSl]|\d)*"  # add later
    regex = r"(?:Page|page)\s*(?:[sSl]|\d)*\s*of\s*(?:[sSl]|\d)*"
    regex2 = r"(S|l|s|\d+)(?=\.*)"
    for file in file_list:
        # print("Filename: ", file)
        for line in open(file):
            # print("line: ", line)
            matches = re.findall(regex, line)
            if len(matches) > 0:
                print("matches: ", matches)
                for i in matches:
                    print("Tuple?: ", i)
            # if len(matches) == 0:
            #     matches = re.findall(regex2, line)
            # if "Page" in line and "of" in line:
            if len(matches) == 1:
                # print("matches: ", matches)
                matched_string = matches[0]
                # print("matching string: ", matched_string)
                page_numbers = re.findall(regex2, matched_string)

                print("page_numbers: ", page_numbers)
                page_num = find_number(page_numbers[0])
                print("Page num: ", page_num)
                page_max = find_number(page_numbers[1])
                print("page max: ", page_max)

                if int(page_num) is not int(page_max):
                    new_name = trans_dir + 'working/images/text/' + str(int(page_num) - 1) + '.txt'
                    os.rename(file, new_name)


                # page_num = matched_string[line_len - 6]
                # if page_num is 'l':
                #     page_num = 1
                # if page_num is 's' or page_num is 'S':
                #     page_num = 5
                #
                # # print("page_num:", page_num)
                #
                # page_max = matched_string[line_len - 1]
                # if page_max is 'l':
                #     page_max = 1
                # if page_max is 's' or page_max is 'S':
                #     page_max = 5
                #
                # # print("page_max:", page_max)
                #
                # if int(page_max) > 1:
                #     if page_num is 'l':
                #         os.rename(file, '1.txt')
                #     else:
                #         new_name = trans_dir + 'working/images/text/' + str(int(page_num) - 1) + '.txt'
                #         # print("Core JST file. New name: ", new_name)
                #         os.rename(file, new_name)


def read_and_scan(text_dir, num, trans_dir):
    saved_course = None
    course_list = []
    file_list = []

    for i in range(0, num - 1):
        print("Converting image to text.. ", i)
        read_command = '(cd ' + text_dir + '; tesseract ../image' + '-' + str(i) + '.jpg image' + '-' + str(i) + ')'
        os.system(read_command)
        filename = text_dir + 'image-' + str(i) + '.txt'
        file_list.append(filename)

    # rearrange files
    # reorder_files(file_list, trans_dir)

    for i in range(0, num - 1):
        print("Scanning text file.. ", i)
        filename = trans_dir + 'working/images/text/image-' + str(i) + '.txt'
        for line in open(filename):
            # if "Military Experience" in line:
                # if saved_course is not None and saved_course not in course_list:
                #     course_list.append(saved_course)
                # return course_list
            if "Credit Is Not Recommended" in line:
                saved_course = None
            if 'MC-' in line or 'NV-' in line or 'AR-' in line or 'CG-' in line or 'AF-' in line or 'DD-' in line \
                    or 'NER-' in line:
                for word in line.split():
                    if word.startswith('MC-') or word.startswith('NV-') or word.startswith('AR-') \
                            or word.startswith('CG-') or word.startswith('DD-') or word.startswith('AF-') \
                            or word.startswith('NER-'):
                        if saved_course is not None and saved_course not in course_list:
                            course_list.append(saved_course)
                        saved_course = word
    return course_list


def grab_jst_courses(trans_dir, jst):
    working_dir = trans_dir + 'working/'
    image_dir = working_dir + 'images/'
    text_dir = image_dir + 'text/'

    clear_dir(working_dir, True)
    copy_file(trans_dir, working_dir, jst)
    convert_to_image(image_dir, jst)

    os.system('mkdir ' + text_dir)
    num_pages = int(os.popen('ls ' + image_dir + ' -1 | wc -l').read())

    course_list = read_and_scan(text_dir, num_pages, trans_dir)
    # clear_dir(working_dir, False)
    return course_list


# Required variables are transcript directory, jst filename, and desired image name
