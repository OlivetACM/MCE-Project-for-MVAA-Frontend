from django.shortcuts import render_to_response
from django.template import RequestContext

from django.views.decorators.csrf import csrf_exempt

from .form import CourseForm, CourseLookup


@csrf_exempt
def index(request):
    print("request recieved")
    if request.method == 'POST':
        form = CourseForm(request.POST)
        data = ""
        if form.is_valid():
            course_lookup = CourseLookup(form.cleaned_data['course_code'])
            data = course_lookup.get_equivalent_courses()

    else:
        form = CourseForm()
        data = ""

    return render_to_response('index.html', {'form': form, 'data': data}, RequestContext(request))
