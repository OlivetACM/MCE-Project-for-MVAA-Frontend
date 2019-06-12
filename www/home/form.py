import logging
import sqlite3

from django import forms

logging.basicConfig(filename='mce.log', level=logging.ERROR)


class CourseForm(forms.Form):
    course_code = forms.CharField(max_length=20)


class CourseLookup:
    def __init__(self, course):
        self.course = course
        self.conn = sqlite3.connect('db.sqlite3', check_same_thread=False)
        self.cursor = self.conn.cursor()

    def get_equivalent_courses(self):
        try:
            self.cursor.execute(
                '''
                    SELECT * FROM dbadmin_course WHERE CourseNumber = ? and CourseEquivalenceNonOC not NULL;
                ''', [self.course])
            results = self.cursor.fetchall()
            return str(self.format_results(results)).replace("'", '"')
        except sqlite3.Error as e:
            logging.error("Error occurred while getting equivalent courses: ", e)
            return ""

    def get_oc_course_info(self, oc_course_code):
        try:
            self.cursor.execute(
                '''
                    SELECT * FROM dbadmin_course WHERE CourseNumber = ?;
                ''', [oc_course_code])

            return str(self.cursor.fetchall())[2:-2].replace("'", "").split(', ')

        except sqlite3.Error as e:
            logging.error("Error occurred while getting OC course description: ", e)
            return ""

    def format_results(self, data_set):
        try:
            data_set = str(data_set)[1:-1].split('), (')
            list_data = []

            for data in data_set:
                dict_data = {}
                new_data = data.replace('(', '').replace(')', "").replace("'", "")
                split_data = new_data.split(', ')

                dict_data["ID"] = split_data[0]
                dict_data["CourseID"] = split_data[1]
                dict_data["CourseNumber"] = split_data[2]
                dict_data["CourseName"] = split_data[3]
                dict_data["CourseDescription"] = str(split_data[4:-4])[1:-1].replace("', '", ", ").replace("'", "")
                dict_data["CourseCredit"] = split_data[-4]
                dict_data["CourseEquivalenceNonOC"] = split_data[-3]

                oc_course_info = self.get_oc_course_info(split_data[-3])
                print(oc_course_info)

                dict_data["OCCourseName"] = oc_course_info[3]
                dict_data["OCCourseDescription"] = oc_course_info[4]
                dict_data["InstitutionID"] = split_data[-2]
                dict_data["ReviewerID"] = split_data[-1]
                list_data.append(dict_data)

            print(list_data)
            return list_data

        except IndexError as e:
            logging.error("Course was not found: ", e)
            return ""
