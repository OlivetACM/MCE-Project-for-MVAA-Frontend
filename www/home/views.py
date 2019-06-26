from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt

from django.http import HttpResponseRedirect

from .form import CourseForm, CourseLookup

from home import jstreader


@csrf_exempt
def index(request):
    form = CourseForm()
    return render_to_response('index.html', {'form': form, 'data': '', 'response': ''}, RequestContext(request))


@csrf_exempt
def pdf_processing(request):
    if request.method == 'POST' and request.FILES['myfile']:
        # try:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        jstreader.clear_dir('documents/jst/', True)
        fs.save("documents/jst/{}".format(myfile.name), myfile)
        jst_list = jstreader.grab_jst_courses('documents/jst/', myfile.name)
        print(jst_list)
        course_lookup = CourseLookup()

        data = str(course_lookup.get_equivalent_courses(jst_list)).replace("'", '"').replace("None", "null")
"""
        #form = CourseForm()
        data = ""
        response = ""
    else:
        form = ""
        data = ""
        response = ""
    
    if request.method == 'POST':
        form = CourseForm(request.POST)
        #course_codes = request.POST.getlist('course_code')
        data = ""
        response = None

        if form.is_valid():
            course_codes = form.cleaned_data['course_code']
            textbox_course = [form.cleaned_data['course_code_text']]

            if course_codes == "" and textbox_course == "":
                response = "No course added"
            else:
                if textbox_course != "":
                    course_codes.append(textbox_course[0])#only one course is entered at a time
                if len(course_codes) != 0:
                    course_codes.sort()
                    data = process_data(course_codes)
    else:
        form = CourseForm()
        data = ""
        response = ""
    

    return render_to_response('index.html', {'form': form, 'data': data, 'response': response}, RequestContext(request))

def process_data(data):
    course_lookup = CourseLookup()
    data = str(course_lookup.get_equivalent_courses(data)).replace("'", '"').replace("None", "null")
    return data
"""
        request.session['processed_data'] = data
        return HttpResponseRedirect('/results')
        # except FileNotFoundError:
        #     response = "The PDF you uploaded is invalid.  Please select a different file."
    else:
        response = "Your request could not be processed, please try again later."

    print(response)
    return render_to_response('error.html', {'response': response}, RequestContext(request))


@csrf_exempt
def single_course_processing(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        courses = []
        if form.is_valid():
            course_code = form.cleaned_data['course_code']
            textbox_course = [form.cleaned_data['course_code_text']]

            courses.append(course_code)
            course_codes.append(textbox_course[0])

            data = str(CourseLookup().get_equivalent_courses(courses)).replace("'", '"').replace("None", "null")
            request.session['processed_data'] = data
            return HttpResponseRedirect('/results')

    response = "Your request could not be processed, please try again later."
    return render_to_response('error.html', {'response': response}, RequestContext(request))


@csrf_exempt
def results(request):
    return render_to_response('results.html',
                              {'data': request.session.get('processed_data'), 'response': ''},
                              RequestContext(request))
