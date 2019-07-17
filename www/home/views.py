from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt

from django.http import HttpResponseRedirect

from .form import CourseForm, CourseLookup, PDFInfo, course_formset
from .render import Render

from . import JSTReader

@csrf_exempt
def index(request):
    form = CourseForm()
    print("--------- view index ------------")
    print("request.session['selected_course_codes'] is: ", request.session.get('selected_course_codes'))
    return render_to_response('index.html', {'form': form, 'data': '', 'response': ''}, RequestContext(request))

@csrf_exempt
def multi_form(request):
    print("--------------multiform----------------")
    preloaded_courses = []
    if request.session.get('jst_dict'):
        for k in request.session.get('jst_dict'):
            for i in request.session.get('jst_dict')[k]:
                preloaded_courses.append(i)

    if preloaded_courses:
        initial = []
        for courses in preloaded_courses:
            initial.append({'name': u'{}'.format(courses)})
        formset = course_formset()(request.GET or None, initial=initial)
    elif request.method == 'GET':
        formset = course_formset()(request.GET or None)
    elif request.method == 'POST':
        formset = course_formset()(request.POST)
    else:
        formset = None
    return render(request, 'multi-form.html', {'formset': formset})


@csrf_exempt
def pdf_processing(request):
    if request.method == 'POST' and request.FILES['myfile']:
        jstreader = JSTReader.JSTReader('documents/jst/')
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        jstreader.clear_dir(True)
        fs.save("documents/jst/{}".format(myfile.name), myfile)
        jst_dict = jstreader.scan_pdf()
        request.session['jst_dict'] = jst_dict
        return HttpResponseRedirect('/multiform')


@csrf_exempt
def course_processing(request):
    print("-----------course_processing------------")
    if request.method == 'POST':
        courses = []
        form = CourseForm(request.POST)
        if form.is_valid():
            print("--------is valid --------")
            checkbox_course_codes = form.cleaned_data['checkbox_course_codes']
            if checkbox_course_codes:
                checkbox_course_codes.sort()
                courses = checkbox_course_codes

            else:
                for i in request.POST:
                    if 'name' in i:
                        courses.append(request.POST[i])

        if courses:
            data = str(CourseLookup().get_equivalent_courses(courses)).replace("'", '"').replace("None", "null")
            request.session['processed_data'] = data
            request.session['course_codes'] = courses

            print("data in course_processing is: ", data)
            return HttpResponseRedirect('/results')

    response = "Your request could not be processed, please try again later."
    return render_to_response('error.html', {'response': response}, RequestContext(request))


@csrf_exempt
def course_information_pdf_processing(request):
    print("-----------course_information_pdf_processing------------")
    if request.method =='POST':
        course_codes = request.session.get('course_codes')
        print("course_codes is: ", course_codes)

        print("--------- view index ------------")
        print("request.session['selected_course_codes'] is: ", request.session.get('selected_course_codes'))

        course_codes.sort()
        #data = str(CourseLookup().get_equivalent_courses(course_code)).replace("'", '"').replace("None", "null")
        accepted_data, elective_data, no_data = CourseLookup().get_equivalent_course_objects(course_codes)
        equivalent_courses = set()
        jst_course_credits_dict = {}

        print("accepted_data is: ", accepted_data)
        print("elective_data is: ", elective_data)
        print("no_data is: ", no_data)

            #pulling equivalent oc courses for each Millitary.
        for sets in accepted_data:#data is a list of sets.
            total_credits = 0
            current_course = sets[0]
            for Course in sets: #sets is made up of Course Objects.
                current_course = Course
                print("current course is: ", Course.CourseNumber)
                oc_course = CourseLookup().get_course(Course.CourseEquivalenceNonOC)
                if oc_course != None:
                    total_credits += float(oc_course.CourseCredit) # adding credits for the current jst.
                    equivalent_courses.add(oc_course)#OC courses do not have equivalant courses filled out.
            jst_course_credits_dict[Course.CourseNumber] = total_credits

            #creating pdfinfo object with to fill in the information and sent it to the PDF form created in render.py
        pdf_info = PDFInfo()
        pdf_info.oc_equivalance = equivalent_courses
        pdf_info.jst_course_credits = jst_course_credits_dict
        pdf_info.selected_courses = accepted_data
        pdf_info.review_courses = no_data

@csrf_exempt
def result(request):
    print("--------- view result ------------")
    print("request.session['course_codes'] is: ", request.session.get('course_codes'))
    #return Render.render('pdf_form.html', {'data': request.session.get('processed_data'),'response':'', 'request':request})
    return render_to_response('results.html', {'data': request.session.get('processed_data'), 'response': ''},
                             RequestContext(request))
