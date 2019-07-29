import sqlite3
from dbadmin.models import Course, Outcome, Reviewer, Institution
from django.core.management.base import BaseCommand

class Command(BaseCommand):

    def handle(self, *args, **options):
        # obj = None
        # Course.objects = None
        print(type(Course.objects))
        print("Loading Database")
        dbname = 'mce.sqlite3'
        conn = sqlite3.connect(dbname)
        curs = conn.cursor()
        curs.execute('select * from Course')
        for row in curs:
            obj = Course.objects.create(
                #CourseID=row[0],
                CourseNumber=row[1],
                CourseName=row[2],
                CourseDescription=row[3],
                CourseCredit=row[4],
                CourseEquivalenceNonOC=row[5],
                InstitutionID=row[6],
                ReviewerID=row[7]
            )
            # print(obj)
        curs.execute('select * from Outcome')
        for row in curs:
            obj2 = Outcome.objects.create(
                #OutcomeID=row[0],
                OutcomeDescription=row[1],
                CourseNumber=row[2]
            )
        curs.execute('select * from Reviewer')
        for row in curs:
            obj3 = Reviewer.objects.create(
                #ReviewerID=row[0],
                ReviewerName=row[1],
                ReviewerPhone=row[2],
                ReviewerEmail=row[3],
                ReviewerDepartment=row[4]
            )
        curs.execute('select * from Institution')
        for row in curs:
            obj4 = Institution.objects.create(
                #InstitutionID=row[0],
                InstitutionName=row[1],
                InstitutionAddress=row[2],
                InstitutionCity=row[3],
                InstitutionState=row[4],
                InstitutionZipcode=row[5],
                InstitutionWebSite=row[6]
            )