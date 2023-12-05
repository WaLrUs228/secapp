import io
import os
import re
import shlex
import subprocess

from django.http import FileResponse, Http404
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
        username = re.sub(r'[^\w]', '', username)
        password = re.sub(r'[^\w]', '', password)
        query = "select * from catalog_myuser where username=? AND password=?;"
        result = models.MyUser.objects.raw(query, [username, password])
        if len(result):
            return redirect('../../profile/' + str(result[0].slug))
        else:
            return render(request, '../templates/registration/login.html', context={'error_msg': 'Your username and password didn\'t match. Please try again.'})

def using_cmd(request):
    if request.method == 'GET':
        return render(request, '../templates/registration/nslookup.html')
    if request.method == 'POST':
        try:
            domain = request.POST.get('domain')
            safe_domain = shlex.quote(domain)
            result = subprocess.check_output('ping ' + safe_domain, shell=True)
            return render(request, '../templates/registration/nslookup.html',
                          context={'result': result.decode().strip()})

        except subprocess.CalledProcessError:
            return render(request, '../templates/registration/nslookup.html',
                          context={'result': 'Invalid input'})


def cool_photo(request):
    filename = request.GET.get('filename')
    if "../" not in filename:
        path = os.path.join('catalog/static/image/', filename)
        if os.path.isfile(path):
            return FileResponse(open(path, 'rb'), content_type='text/plain')
    else:
        raise Http404

def logout(request):

    return render(request, '../templates/registration/logged_out.html')