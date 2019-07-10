from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt

from django.http import HttpResponseRedirect

from .form import CourseForm, CourseLookup
from .render import Render

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
        course_lookup = CourseLookup()

        data = str(course_lookup.get_equivalent_courses(jst_list)).replace("'", '"').replace("None", "null")
        
        request.session['processed_data'] = data
        return HttpResponseRedirect('/results')
        # except FileNotFoundError:
        #     response = "The PDF you uploaded is invalid.  Please select a different file."
    else:
        response = "Your request could not be processed, please try again later."

    return render_to_response('error.html', {'response': response}, RequestContext(request))


@csrf_exempt
def single_course_processing(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        courses = []
        if form.is_valid():
            course_code = form.cleaned_data['course_code']
            textbox_course = [form.cleaned_data['course_code_text']]
            
            course_code.append(textbox_course[0])


            course_code.sort()
            #data = str(CourseLookup().get_equivalent_courses(course_code)).replace("'", '"').replace("None", "null")
            data = CourseLookup().get_equivalent_courses(course_code)
            equivalent_courses = []

            #pulling equivalent oc courses for each Millitary.
            for sets in data:#data is a list of sets.
                for Course in sets:#sets is made up of Course Objects.
                    equivalent_courses.append(CourseLookup().search_database(Course.CourseEquivalenceNonOC, equivalant_check=True))#OC courses do not have equivalant courses filled out.

            return Render.render('pdf_form.html', {'data': data, 'equivalent_courses': equivalent_courses, 'response':'', 'request':request})#, 'equivalent_courses': equivalent_courses
            #request.session['processed_data'] = data
            #return HttpResponseRedirect('/result')

    response = "Your request could not be processed, please try again later."
    return render_to_response('error.html', {'response': response}, RequestContext(request))


@csrf_exempt
def result(request):
    return Render.render('pdf_form.html', {'data': request.session.get('processed_data'),'response':'', 'request':request})
    #return render_to_response('results.html',
     #                         {'data': request.session.get('processed_data'), 'response': ''},
      #                        RequestContext(request))
