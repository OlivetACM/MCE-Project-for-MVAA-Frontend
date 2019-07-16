import logging
from django import forms
from django.forms import formset_factory

from dbadmin.models import Course

logging.basicConfig(filename='mce.log', level=logging.ERROR)


"""CourseCodes is used to generate a query of Course objects where they have a 
       equivalant Olivet course. It then creats a set and then fills it with touples
       of Course numbers that then gets returned in the iter function
    """
class CourseCodes(object):
    def __init__(self):
        self.query = Course.objects.filter(CourseEquivalenceNonOC__isnull=False,).exclude(CourseName__exact='', CourseDescription__exact='')
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
    checkbox_course_codes = forms.MultipleChoiceField(choices=course_code_choices, initial='', widget=forms.CheckboxSelectMultiple(), required=False)#MultipleChoiceField() works the best with Checkboxselectmultiple()
    course_code = forms.CharField(max_length=30, required=False)


class CourseLookup:
    def __init__(self):
        self.number_of_oc_courses = 0.0
        self.number_of_approved_credits = 0.0

    def get_equivalent_courses(self, requested_courses):
        database_result = {'Data': []}
        # requested_courses = requested_courses.split(" ")   # NEEDS TO CHANGE AS LIST WILL BE `requested_courses`
        i = 0
        for course in requested_courses:
            data = self.search_database(course)
            if data:
                database_result['Data'].append(data)
                i += 1
        print(database_result)
        return database_result

    def search_database(self, course_number):
        database_data = Course.objects.filter(CourseNumber=course_number, CourseEquivalenceNonOC__isnull=False)
        return self.format_results(database_data)

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
            return combined_courses

        except IndexError as e:
            logging.error("Course was not found: ", e)
            return ""
          
          
        # used for returning a list of database objects
    def get_equivalent_course_objects(self, requested_courses):
        database_result = []
        for course in requested_courses:
            if course:
                data = self.search_database_object(course)
                if data:
                    database_result.append(data)
        return database_result

    #used to search the database for jst courses.
    def search_database_object(self, course_number, equivalant_check=False):
        database_data = Course.objects.filter(CourseNumber=course_number, CourseEquivalenceNonOC__isnull=equivalant_check)
        if equivalant_check == True:
            if database_data:
                print("in search_database: ", database_data)
            
        return database_data

    # used to get a course object.
    def get_course(self, course_code):
        try:
            return Course.objects.get(CourseNumber=course_code)
        except Exception as e:
            print("!!!!!Course Equivalant ", course_code, " Not found In DataBase!!!!!")


# used in sending info to pdf
class PDFINFO:
    selected_courses = {}
    oc_equivilance = {}
    jst_course_credits = []
    courses = {}





















