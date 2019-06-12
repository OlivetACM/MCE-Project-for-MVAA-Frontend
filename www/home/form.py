import sqlite3

from django import forms


class CourseForm(forms.Form):
    course_code = forms.CharField(max_length=20)

class CourseLookup:
    def __init__(self, course):
        self.course = course
        self.conn = sqlite3.connect('db.sqlite3', check_same_thread=False)
        self.cursor = self.conn.cursor()

    def get_equivalent_courses(self, course_code):
        self.cursor.execute('''SELECT * FROM course WHERE CourseNumber = ? and CourseEquivalenceNonOC not NULL;''', [course_code])
        results = self.cursor.fetchall()
        return str(self.format_results(results)).replace("'", '"')

    def get_oc_course_description(self, course_code):
        self.cursor.execute('''SELECT CourseDescription FROM course WHERE CourseNumber = ?''', [course_code])
        return self.cursor.fetchall()

    def format_results(self, data_set):
        data_set = str(data_set)[1:-1].split('), (')
        list_data = []

        for data in data_set:
            dict_data = {}
            new_data = data.replace('(', '').replace(')', "").replace("'", "")
            split_data = new_data.split(', ')

            dict_data["CourseID"] = split_data[0]
            dict_data["CourseNumber"] = split_data[1]
            dict_data["CourseName"] = split_data[2]
            dict_data["CourseDescription"] = str(split_data[3:-4])[1:-1].replace("', '", ", ").replace("'", "")
            dict_data["CourseCredit"] = split_data[-3]
            dict_data["CourseEquivalenceNonOC"] = split_data[-2]
            dict_data["CourseDescriptionNonOC"] = str(self.get_oc_course_description(split_data[-2]))[3:-4]
            dict_data["InstitutionID"] = split_data[-1]
            list_data.append(dict_data)

        return list_data
