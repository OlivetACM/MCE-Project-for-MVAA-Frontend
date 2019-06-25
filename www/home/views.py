from django.shortcuts import render_to_response
from django.template import RequestContext

from django.core.files.storage import FileSystemStorage

from django.views.decorators.csrf import csrf_exempt

from .form import CourseForm, CourseLookup

import json
import ast


@csrf_exempt
def index(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        fs.save("documents/jst/{}".format(myfile.name), myfile)

        form = CourseForm()
        data = ""
        response = ""

    elif request.method == 'POST':
        form = CourseForm(request.POST)
        #course_codes = request.POST.getlist('course_code')
        data = ""
        response = None

        if form.is_valid():
            course_codes = form.cleaned_data['course_code']
            textbox_course = []
            textbox_course.append(form.cleaned_data['course_code_text'])
            print("course_codes is: ", course_codes)

            if course_codes == "" and textbox_course == "":
                response = "No course added"
            else:
                course_lookup = CourseLookup()

                data = str(course_lookup.get_equivalent_courses(course_code)).replace("'", '"').replace("None", "null")
    else:
        form = CourseForm()
        data = ""
        response = ""

    return render_to_response('index.html', {'form': form, 'data': data, 'response': response}, RequestContext(request))
