import sqlite3


class Course:

    def __init__(self, dbname, num):
        # Establish connection to the database
        conn = sqlite3.connect(dbname)
        curs = conn.cursor()

        self.number = num
        self.name = ''.join(curs.execute('select CourseName from dbadmin_course where '
                                         'CourseNumber=?', (num,)).fetchone())
        self.description = ''.join(curs.execute('select CourseDescription from dbadmin_course where CourseNumber=?',
                                                (num,)).fetchone())
        self.outcomes = list(map(lambda x: x[0], curs.execute('select OutcomeDescription from dbadmin_outcome where '
                                                              'CourseNumber=?', (num,)).fetchall()))

