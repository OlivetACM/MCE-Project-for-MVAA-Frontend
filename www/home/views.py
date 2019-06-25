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
            textbox_course = []
            textbox_course.append(form.cleaned_data['course_code_text'])
            print("course_codes is: ", course_codes)

            if course_codes == "" and textbox_course == "":
                response = "No course added"
            else:
                course_lookup = CourseLookup()
                look_up_course = ""
                if textbox_course == "":
                    look_up_course = course_codes
                else:
                    look_up_course = textbox_course
                print("running course_lookup")
                print("look_up_course is: ", look_up_course)
                data = course_lookup.get_equivalent_courses(look_up_course)
    else:
        form = CourseForm()
        data = ""
        response = ""

    return render_to_response('index.html', {'form': form, 'data': data, 'response': response}, RequestContext(request))
