import django.utils.html
from django.shortcuts import render
from django.views import generic

from .models import Chat, MyUser
from django.contrib.auth.models import User

def index(request, pk):
    if request.method == 'POST':
        user_pk = request.build_absolute_uri()[30:-1]
        user = MyUser.objects.get(pk=user_pk)
        new_msg = Chat(author=user.username, text=request.POST.get('msg'))
        new_msg.save()

    #if request.method == 'GET':
    entry = MyUser.objects.get(pk=pk)
    username = entry.username
    chat = Chat.objects.all()
    for msg in chat:
        msg.text = django.utils.html.mark_safe(django.utils.html.escape(msg.text))
    return render(
        request,
        'index.html',
        context={'username':username, 'chat':chat},
    )