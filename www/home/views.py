from django.shortcuts import render_to_response
from django.template import RequestContext

from django.views.decorators.csrf import csrf_exempt

from .form import CourseForm, CourseLookup


@csrf_exempt
def index(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        #course_codes = request.POST.getlist('course_code')
        data = ""
        response = None

        if form.is_valid():
            course_codes = form.cleaned_data['course_code']

            if course_codes == "":
                response = "No course added"
            else:
                course_lookup = CourseLookup()
                data = course_lookup.get_equivalent_courses(course_codes)
    else:
        form = CourseForm()
        data = ""
        response = ""

    return render_to_response('index.html', {'form': form, 'data': data, 'response': response}, RequestContext(request))
