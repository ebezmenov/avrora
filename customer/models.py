# coding: UTF8
from django.db import models
from django.contrib.auth.models import User

class CustomerProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    
    discount = models.IntegerField(u"Скидка")
