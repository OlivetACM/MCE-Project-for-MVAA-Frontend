from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from flask import Flask, request
app = Flask(__name__)

import requests

data = {}


def index(request):
    return render(request, 'index.html', context={"data": data})


def submit(request):
    course_code = request.POST['course_code']
    web_hook_url = "http://127.0.0.1:5001"

    r = requests.post(web_hook_url, course_code)

    return HttpResponseRedirect('/')


# @app.route('/', methods=['POST'])
# def web_hook():
#     if request.method == 'POST':
#         global data
#         data = request.data
