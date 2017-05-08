from __future__ import unicode_literals
from django.utils.timezone import now
from django.db import models
import bcrypt

class UserManager(models.Manager):
    def register_user(self, form_data):
        password = form_data['password']
        hashed = bcrypt.hashpw(str(password), bcrypt.gensalt())
        user = User.objects.create(first_name=form_data['first_name'], last_name=form_data['last_name'], email=form_data['email'], password=hashed)
        user.save()
        return user

class User(models.Model):
    first_name =  models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    objects = UserManager()

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)
