from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response, render
from django.template import RequestContext
import dbadmin.CourseComparisonMaterial.CourseComparison as CourseComparison

from dbadmin.models import Course, Reviewer

# Create your views here.

@csrf_exempt
def equivalency(request):
    data = []
    all_course_codes = CourseNumbers()
    courses_and_descriptions = CourseNumbers().course_and_descriptions
    all_course_codes = sorted(all_course_codes)
    data.append(all_course_codes)
    data.append(courses_and_descriptions)
    if (request.method == 'POST'):
        course_pair = [request.POST.get('inst_course'), request.POST.get('military_course'), CourseNumbers().find_reviewer(request.POST.get('inst_course'))]
        print(course_pair)
        if (course_pair[2] != ''):
            CourseComparison.make_comparison(course_pair)
    return render_to_response('admin/equivalency.html', {'data': data, 'response': ''},
                              RequestContext(request))

class CourseNumbers(object):


    def __init__(self):
        self.all_courses = Course.objects.all()
        self.all_reviewers = Reviewer.objects.all()
        for i in self.all_reviewers:
            print("reviewer is: ", i.ReviewerName)
        self.all_course_codes = set()
        self.course_and_descriptions = []
        for course in self.all_courses:
            self.all_course_codes.add((course.CourseNumber, course.InstitutionID))
            self.course_and_descriptions.append((course.CourseNumber, course.CourseDescription))
            #self.courses_instructor[course.CourseNumber] = course.ReviewerID

    def __iter__(self):
        return iter(self.all_course_codes)

    def find_reviewer(self, course):
        reviewerName = ""
        for c in self.all_courses:
            if(c.CourseNumber == course):
                try:
                    reviewer = self.all_reviewers[c.ReviewerID-1]
                    print("reviewer is: ", reviewer)
                    reviewerName = reviewer.ReviewerName
                except:
                    pass
        return reviewerName

