
from django.db import models

from django.contrib.auth.models import AbstractBaseUser


class MyUser(AbstractBaseUser):
    username = models.CharField(max_length=30, verbose_name="username")
    password = models.CharField(max_length=128, verbose_name="password")
    slug = models.SlugField()
    USERNAME_FIELD = 'username'

    def __str__(self):
        return '%s, %s' % (self.pk, self.username)

class Chat(models.Model):

    text = models.CharField(max_length=200)
    author = models.CharField(max_length=20)

    def __str__(self):
        return self.text, self.author


class TemporaryBanIp(models.Model):
    class Meta:
        db_table = "TemporaryBanIp"

    ip_address = models.GenericIPAddressField("IP address")
    attempts = models.IntegerField("Attempts", default=0)
    time_unblock = models.DateTimeField("Time", blank=True)
    status = models.BooleanField("Status", default=False)

    def __str__(self):
        return self.ip_address