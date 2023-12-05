import os
import re
import shlex
import subprocess

from django.http import FileResponse, Http404
from django.shortcuts import render
from catalog import models
from django.shortcuts import redirect
from django.utils import timezone


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def custom_login(request):
    if request.method == 'GET':
        ip = get_client_ip(request)
        return render(request, '../templates/registration/login.html', context={'error_msg': ''})
    if request.method == 'POST':
        ip = get_client_ip(request)
        obj, created = models.TemporaryBanIp.objects.get_or_create(
            defaults = {
                'ip_address': ip,
                'time_unblock': timezone.now()
            },
            ip_address=ip
        )

        if obj.status is True and obj.time_unblock > timezone.now():
            if obj.attempts == 3:
                return render(request, '../templates/registration/login.html',
                              context={'error_msg': 'Too many attempts. Relax.'})

        elif obj.status is True and obj.time_unblock < timezone.now():
            obj.status = False
            obj.save()

        username = request.POST.get('username')
        password = request.POST.get('password')
        username = re.sub(r'[^\w]', '', username)
        password = re.sub(r'[^\w]', '', password)
        query = "select * from catalog_myuser where username=%s AND password=%s;"
        result = models.MyUser.objects.raw(query, [username, password])
        if len(result):
            obj.attempts = 0
            obj.save()
            return redirect('../../profile/' + str(result[0].slug))
        else:
            obj.attempts += 1
            if obj.attempts == 3:
                obj.time_unblock = timezone.now() + timezone.timedelta(minutes=5)
                obj.status = True
            obj.save()
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
