import io
import os
import subprocess

from django.http import FileResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from catalog import models
from django.shortcuts import redirect

'''
query = "select * from auth_user where username='qwerty' AND password='qetadg123';"
>>> results = User.objects.raw(query)                                                   
>>> for result in results:
...     result

'''

def custom_login(request):
    if request.method == 'GET':
        return render(request, '../templates/registration/login.html', context={'error_msg': ''})
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        result = models.MyUser.objects.raw("select * from catalog_myuser where username='" + username + "' AND password='" + password + "';")
        if len(result):
            return redirect('../../profile/' + str(result[0].pk))
        else:
            return render(request, '../templates/registration/login.html', context={'error_msg': 'Your username and password didn\'t match. Please try again.'})

def using_cmd(request):
    if request.method == 'GET':
        return render(request, '../templates/registration/nslookup.html')
    if request.method == 'POST':
        domain = request.POST.get('domain')
        result = subprocess.check_output('ping ' + domain, shell=True)
        return render(request, '../templates/registration/nslookup.html', context={'result':result.decode().strip()})

def cool_photo(request):
    filename = request.GET.get('filename')
    path = os.path.join('catalog/static/image/', filename)
    if os.path.isfile(path):
        return FileResponse(open(path, 'rb'), content_type='text/plain')