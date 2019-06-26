from django.shortcuts import render_to_response
from django.template import RequestContext

from django.core.files.storage import FileSystemStorage

from django.views.decorators.csrf import csrf_exempt

from .form import CourseForm, CourseLookup

import json
import ast
from home import jstreader


@csrf_exempt
def index(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        jstreader.clear_dir('documents/jst/', True)
        fs.save("documents/jst/{}".format(myfile.name), myfile)
        jst_list = jstreader.grab_jst_courses('documents/jst/', myfile.name)
        print(jst_list)
        course_lookup = CourseLookup()

        data = str(course_lookup.get_equivalent_courses(jst_list)).replace("'", '"').replace("None", "null")
        form = CourseForm()
        # data = ""
        response = ""

    elif request.method == 'POST':
        form = CourseForm(request.POST)
        data = ""
        response = None
        if form.is_valid():
            course_code = form.cleaned_data['course_code']
            if course_code == "":
                response = "No course added"
            else:
                course_lookup = CourseLookup()

                data = str(course_lookup.get_equivalent_courses(course_code)).replace("'", '"').replace("None", "null")

    else:
        form = CourseForm()
        data = ""
        response = ""

    return render_to_response('index.html', {'form': form, 'data': data, 'response': response}, RequestContext(request))
