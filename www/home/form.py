import logging
from django import forms
from django.forms import formset_factory

from dbadmin.models import Course

logging.basicConfig(filename='mce.log', level=logging.ERROR)


class CourseCodes(object):
    """
    CourseCodes is used to generate a query of Course objects where they have a
    equivalant Olivet course. It then creats a set and then fills it with touples
    of Course numbers that then gets returned in the iter function
    """
    def __init__(self):
        self.query = Course.objects.filter(CourseEquivalenceNonOC__isnull=False,).exclude(
            CourseName__exact='', CourseDescription__exact='')
        self.course_numbers = set()
        for i in self.query:
            self.course_numbers.add((i.CourseNumber, i.CourseNumber))

    def __iter__(self):
        return iter(self.course_numbers)
    

class CourseForm(forms.Form):
    """CourseForm sets up the container that will be displayed in the html by {{form}}
       ChoiceFields is the form template being used currently that sets up a list drop
       down filled with choices provided by CoursCodes. Check django docs for more
       information on ChoicField()
    """
    course_code_choices = sorted(CourseCodes())

    # MultipleChoiceField() works the best with CheckboxSelectMultiple()
    checkbox_course_codes = forms.MultipleChoiceField(choices=course_code_choices,
                                                      initial='',
                                                      widget=forms.CheckboxSelectMultiple(),
                                                      required=False)
    course_code = forms.CharField(max_length=30, required=False)


class MultiCourseForm(forms.Form):
    __name__ = ""
    name = forms.CharField(
        label='Course Name',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Course Name here'
        })
    )


def course_formset(fields=1):
    multi_course_form_set = formset_factory(MultiCourseForm, extra=fields)
    return multi_course_form_set


class CourseLookup:
    def __init__(self):
        self.number_of_oc_courses = 0.0
        self.number_of_approved_credits = 0.0

    def get_equivalent_courses(self, requested_courses):
        database_result = {'Data': [], 'NoEquivalencies': []}
        for course in requested_courses:
            data = self.search_database(course)
            if data:
                database_result['Data'].append(data)
            else:
                database_result['NoEquivalencies'].append(course)
        return database_result

    def search_database(self, course_number):
        database_data = Course.objects.filter(CourseNumber=course_number, CourseEquivalenceNonOC__isnull=False)
        return self.format_results(database_data)

    def format_results(self, database_data):
        print("------------format_results------------")
        try:
            combined_courses = []
            for course in database_data:
                print("-----------looking through courses -----------")
                self.number_of_oc_courses += 1
                formatted_courses = {}
                #formatted_courses["CourseID"] = course.CourseID
                formatted_courses["CourseNumber"] = course.CourseNumber
                formatted_courses["CourseName"] = course.CourseName
                formatted_courses["CourseDescription"] = course.CourseDescription
                formatted_courses["CourseCredit"] = course.CourseCredit
                self.number_of_approved_credits += float(course.CourseCredit)

                print("Course.objects.get(CourseNumber=course.CourseEquivalenceNonOC) is: ", Course.objects.get(CourseNumber=course.CourseEquivalenceNonOC))

                course_equivalence_non_oc_data = Course.objects.get(CourseNumber=course.CourseEquivalenceNonOC)
                print("course_equivalence_non_oc_data is: ", course_equivalence_non_oc_data)
                formatted_courses["CourseEquivalenceNonOC"] = course.CourseEquivalenceNonOC
                formatted_courses["OCCourseName"] = course_equivalence_non_oc_data.CourseName
                formatted_courses["OCCourseDescription"] = course_equivalence_non_oc_data.CourseDescription

                formatted_courses["InstitutionID"] = course.InstitutionID
                formatted_courses["ReviewerID"] = course.ReviewerID
                combined_courses.append(formatted_courses)
                print("----------returning in format_results-----------")
            return combined_courses

        except IndexError as e:
            logging.error("Course was not found: ", e)
            return ""
          
          
     # used for returning a list of database objects

    def get_equivalent_course_objects(self, requested_courses):
        # used for returning a list of database objects
        database_result = []
        courses_non_equivalence = []
        no_data = []
        for course in requested_courses:
            if course:
                data = self.search_database_object(course)
                if data:
                    database_result.append(data)
                else:
                    no_equivalence = self.search_database_object(course, equivalant_check=True).exclude(CourseName__exact='', CourseDescription__exact='')
                    if no_equivalence:
                        courses_non_equivalence.append(no_equivalence)
                    else:
                        no_data.append(course)


        return database_result, courses_non_equivalence, no_data


    #used to search the database for jst courses.
    def search_database_object(self, course_number, equivalant_check=False):
        database_data = Course.objects.filter(CourseNumber=course_number, CourseEquivalenceNonOC__isnull=equivalant_check)
        if equivalant_check:
            if database_data:
                print("in search_database: ", database_data)
            
        return database_data

    @staticmethod
    def get_course(course_code):
        # used to get a course object.
        try:
            return Course.objects.get(CourseNumber=course_code)
        except IndexError as e:
            logging.error("Course was not found: ", e)
            return ""


# used in sending info to pdf
class PDFInfo:


    #Used for filling out Accepted JST Section of PDF
    selected_courses = {}
    oc_equivalance = {}
    jst_course_credits = []

    #Used for filling out Courses in review Section of PDF
    review_courses = {}

    #Used for filling out General Elective Credits fo PDF
    elective_courses = []




















