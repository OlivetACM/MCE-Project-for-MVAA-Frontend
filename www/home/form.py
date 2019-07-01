import logging
from django import forms
from dbadmin.models import Course

logging.basicConfig(filename='mce.log', level=logging.ERROR)

"""CourseCodes is used to generate a query of Course objects where they have a 
   equivalant Olivet course. It then creats a set and then fills it with touples
   of Course numbers that then gets returned in the iter function
"""
class CourseCodes(object):
    def __init__(self):
        self.query = Course.objects.filter(CourseEquivalenceNonOC__isnull=False,)
        self.course_numbers = set()
        for i in self.query:
            self.course_numbers.add((i.CourseNumber, i.CourseNumber))
    def __iter__(self):
        return iter(self.course_numbers)

"""CourseForm sets up the container that will be displayed in the html by {{form}}
   ChoiceFields is the form template being used currently that sets up a list drop 
   down filled with choices provided by CoursCodes. Check django docs for more 
   information on ChoicField()
"""
class CourseForm(forms.Form):
    course_code_choices = sorted(CourseCodes())
    course_code_text = forms.CharField(max_length=30, required=False)
    course_code = forms.MultipleChoiceField(choices=course_code_choices, initial='', widget=forms.CheckboxSelectMultiple(), required=False)#MultipleChoiceField() works the best with Checkboxselectmultiple()

class CourseLookup:
    def __init__(self):
        pass

    def get_equivalent_courses(self, requested_courses):
        database_result = []
        # requested_courses = requested_courses.split(" ")   # NEEDS TO CHANGE AS LIST WILL BE `requested_courses`
        for course in requested_courses:
            if course:
                data = self.search_database(course)
                if data:
                    database_result.append(data)
        return database_result

    def search_database(self, course_number):
        database_data = Course.objects.filter(CourseNumber=course_number, CourseEquivalenceNonOC__isnull=False)
        print("database_data is: ", database_data)
        return self.format_results(database_data)

    def format_results(self, database_data):
        try:
            combined_courses = []
            for course in database_data:
                formatted_courses = {}
                formatted_courses["CourseID"] = course.CourseID
                formatted_courses["CourseNumber"] = course.CourseNumber
                formatted_courses["CourseName"] = course.CourseName
                formatted_courses["CourseDescription"] = course.CourseDescription
                formatted_courses["CourseCredit"] = course.CourseCredit
                try:
                    course_equivalence_non_oc_data = Course.objects.get(CourseNumber=course.CourseEquivalenceNonOC)
                except Exception as e:
                    print("!!!!!Course Equivalant ", course.CourseEquivalenceNonOC, " Not found In DataBase!!!!!")
                    formatted_courses["CourseCredit"] = "undefined"
                    combined_courses.append(formatted_courses)
                    return combined_courses
                formatted_courses["CourseEquivalenceNonOC"] = course.CourseEquivalenceNonOC
                formatted_courses["OCCourseName"] = course_equivalence_non_oc_data.CourseName
                formatted_courses["OCCourseDescription"] = course_equivalence_non_oc_data.CourseDescription

                formatted_courses["InstitutionID"] = course.InstitutionID
                formatted_courses["ReviewerID"] = course.ReviewerID
                combined_courses.append(formatted_courses)
            #print(combined_courses)
            return combined_courses

        except IndexError as e:
            logging.error("Course was not found: ", e)
            return ""
