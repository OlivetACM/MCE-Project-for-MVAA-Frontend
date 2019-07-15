import logging
from django import forms

from dbadmin.models import Course

logging.basicConfig(filename='mce.log', level=logging.ERROR)


class CourseForm(forms.Form):
    course_code = forms.CharField(max_length=30)


class CourseLookup:
    def __init__(self):
        self.number_of_oc_courses = 0
        self.number_of_approved_credits = 0

    """ !!!!get_equivalent_courses and search_database have been modifies to send to pdf check older version to see
        how to send information to results page.!!!!
    """
    def get_equivalent_courses(self, requested_courses):
        database_result = {}
        # requested_courses = requested_courses.split(" ")   # NEEDS TO CHANGE AS LIST WILL BE `requested_courses`
        for course in requested_courses:
            data = self.search_database(course)
            if data:
                database_result["Data"] = [data]
                database_result["MetaData"] = {"ApprovedCredits": self.number_of_approved_credits,
                                               "NumberOfJSTCourses": len(requested_courses),
                                               "NumberOfOCCourses": self.number_of_oc_courses}
        return database_result

    def search_database(self, course_number):
        database_data = Course.objects.filter(CourseNumber=course_number, CourseEquivalenceNonOC__isnull=False)
        return self.format_results(database_data)

    def search_database(self, course_number, equivalant_check=False):
        database_data = Course.objects.filter(CourseNumber=course_number, CourseEquivalenceNonOC__isnull=equivalant_check)
        if equivalant_check == True:
            if database_data:
                print("in search_database: ", database_data)
            
        return database_data

    def get_course(self, course_code):
        try:
            return Course.objects.get(CourseNumber=course_code)
        except Exception as e:
            print("!!!!!Course Equivalant ", course_code, " Not found In DataBase!!!!!")

    def format_results(self, database_data):
        try:
            print(database_data)
            combined_courses = []
            for course in database_data:
                self.number_of_oc_courses += 1
                formatted_courses = {}
                formatted_courses["CourseID"] = course.CourseID
                formatted_courses["CourseNumber"] = course.CourseNumber
                formatted_courses["CourseName"] = course.CourseName
                formatted_courses["CourseDescription"] = course.CourseDescription
                formatted_courses["CourseCredit"] = course.CourseCredit
                self.number_of_approved_credits += float(course.CourseCredit)

                course_equivalence_non_oc_data = Course.objects.get(CourseNumber=course.CourseEquivalenceNonOC)
                formatted_courses["CourseEquivalenceNonOC"] = course.CourseEquivalenceNonOC
                formatted_courses["OCCourseName"] = course_equivalence_non_oc_data.CourseName
                formatted_courses["OCCourseDescription"] = course_equivalence_non_oc_data.CourseDescription

                formatted_courses["InstitutionID"] = course.InstitutionID
                formatted_courses["ReviewerID"] = course.ReviewerID
                combined_courses.append(formatted_courses)
            print(combined_courses)
            print(self.number_of_approved_credits)
            return combined_courses

        except IndexError as e:
            logging.error("Course was not found: ", e)
            return ""

# used in sending info to pdf
class PDFINFO:
    selected_courses = {}
    oc_equivilance = {}
    jst_course_credits = []
    courses = {}





















