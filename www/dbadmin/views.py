from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response, render
from django.template import RequestContext

from dbadmin.models import Course

# Create your views here.

@csrf_exempt
def equivalency(request):
    if(request.method == 'POST'):
        print("this is a post request")
        #request.POST.get('school_course')
    all_course_codes = CourseNumbers()
    all_course_codes = sorted(all_course_codes)
    return render_to_response('admin/equivalency.html', {'data': all_course_codes, 'response': ''},
                              RequestContext(request))

class CourseNumbers(object):


    def __init__(self):
        all_courses = Course.objects.all()
        self.all_course_codes = set()
        for course in all_courses:
            self.all_course_codes.add((course.CourseNumber, course.InstitutionID))

    def __iter__(self):
        return iter(self.all_course_codes)
