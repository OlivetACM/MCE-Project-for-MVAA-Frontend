from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt


import requests

from .form import CourseForm, CourseLookup

def index(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            CourseLookup(form.cleaned_data['course_code'])
            return HttpResponseRedirect('/')
    else:
        form = CourseForm()

    return render(request, 'index.html', {'form': form})






















# data = None

# @csrf_exempt
# def index(request):
#     global data
#     if request.method == 'POST':
#         data = str(request.body.decode('utf-8'))
#         data = data[2: -1]
#     elif request.method == 'GET':
#         display_data = data
#         data = ""
#         return render(request, 'index.html', context={"data": display_data})
#
#     return render(request, 'index.html', context={"data": ""})
#
#
# def submit(request):
#     global data
#     data = ""
#     course_code = request.POST['course_code']
#     web_hook_url = "http://127.0.0.1:5001"
#
#     r = requests.post(web_hook_url, course_code)
#
#     return HttpResponseRedirect('/')
