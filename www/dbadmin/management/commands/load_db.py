import sqlite3
from dbadmin.models import Course
from django.core.management.base import BaseCommand

class Command(BaseCommand):

    def handle(self, *args, **options):
        print("Loading Database")
        dbname = 'mce.sqlite3'
        conn = sqlite3.connect(dbname)
        curs = conn.cursor()
        curs.execute('select * from Course')
        for row in curs:
            obj = Course.objects.create(
                CourseID = row[0],
                CourseNumber = row[1],
                CourseName = row[2],
                CourseDescription = row[3],
                CourseCredit = row[4],
                CourseEquivalenceNonOC = row[5],
                InstitutionID = row[6],
                ReviewerID = row[7]
            )
            print(obj)
