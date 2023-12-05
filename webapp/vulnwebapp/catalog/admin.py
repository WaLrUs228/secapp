from django.contrib import admin
from .models import Chat, MyUser, TemporaryBanIp

admin.site.register(Chat)
admin.site.register(MyUser)
admin.site.register(TemporaryBanIp)
