from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt

from django.http import HttpResponseRedirect

from .form import CourseForm, CourseLookup, PDFINFO
from .render import Render

from home import JSTReader


@csrf_exempt
def index(request):
    form = CourseForm()
    print("--------- view index ------------")
    print("request.session['selected_course_codes'] is: ", request.session.get('selected_course_codes'))
    return render_to_response('index.html', {'form': form, 'data': '', 'response': ''}, RequestContext(request))


@csrf_exempt
def pdf_processing(request):
    if request.method == 'POST' and request.FILES['myfile']:
        jstreader = JSTReader.JSTReader('documents/jst/')
        # try:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        jstreader.clear_dir(True)
        fs.save("documents/jst/{}".format(myfile.name), myfile)
        jst_dict = jstreader.scan_pdf()
        course_lookup = CourseLookup()

        data = str(course_lookup.get_equivalent_courses(jst_dict['accepted'])).replace("'", '"').replace("None", "null")
        
        request.session['processed_data'] = data
        request.session['selected_course_codes'] = jst_dict['accepted']

        print("--------- view pdf_processing ------------")
        print("request.session['selected_course_codes'] is: ", request.session.get('selected_course_codes'))

        return HttpResponseRedirect('/results')
        # except FileNotFoundError:
        #     response = "The PDF you uploaded is invalid.  Please select a different file."
    else:
        response = "Your request could not be processed, please try again later."

    return render_to_response('error.html', {'response': response}, RequestContext(request))


@csrf_exempt
def course_processing(request):
    print("-----------course_processing------------")
    if request.method == 'POST':
        form = CourseForm(request.POST)
        courses = []
        if form.is_valid():
            print("--------is valid --------")
            checkbox_course_codes = form.cleaned_data['checkbox_course_codes']
            course_code = [form.cleaned_data['course_code']]
            
            print("------------apending to checkbox_course_codes--------------")
            checkbox_course_codes.append(course_code[0])

            checkbox_course_codes.sort()
            data = str(CourseLookup().get_equivalent_courses(checkbox_course_codes)).replace("'", '"').replace("None", "null")
            request.session['processed_data'] = data
            request.session['selected_course_codes'] = checkbox_course_codes

            print("data in course_processing is: ", data)


            return HttpResponseRedirect('/results')

    response = "Your request could not be processed, please try again later."
    return render_to_response('error.html', {'response': response}, RequestContext(request))


@csrf_exempt
def course_information_pdf_processing(request):
    print("-----------course_information_pdf_processing------------")
    if request.method =='POST':
        course_codes = request.session.get('selected_course_codes')
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
        pdf_info = PDFINFO()
        pdf_info.oc_equivilance = equivalent_courses
        pdf_info.jst_course_credits = jst_course_credits_dict
        pdf_info.selected_courses = accepted_data
        pdf_info.review_courses = no_data

@csrf_exempt
def result(request):
    print("--------- view result ------------")
    print("request.session['selected_course_codes'] is: ", request.session.get('selected_course_codes'))
    #return Render.render('pdf_form.html', {'data': request.session.get('processed_data'),'response':'', 'request':request})
    return render_to_response('results.html', {'data': request.session.get('processed_data'), 'response': ''},
                             RequestContext(request))
