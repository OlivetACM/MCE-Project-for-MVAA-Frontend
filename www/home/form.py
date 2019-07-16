import logging
from django import forms
from django.forms import formset_factory

from dbadmin.models import Course

logging.basicConfig(filename='mce.log', level=logging.ERROR)


class CourseForm(forms.Form):
    name = forms.CharField(
        label='Course Code',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter course code here'
        })
    )


def form_factory(num_fields):
    return formset_factory(CourseForm, extra=num_fields)


class CourseLookup:
    def __init__(self):
        self.number_of_oc_courses = 0
        self.number_of_approved_credits = 0

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
