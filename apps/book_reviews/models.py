from __future__ import unicode_literals

from django.db import models
from ..login_registration.models import User

class Author(models.Model):
    name = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # books

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=45)
    author = models.ForeignKey(Author, related_name='books')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #reviews

    def __str__(self):
        return self.title

class Review(models.Model):
    rating = models.IntegerField()
    review_text = models.TextField()
    book = models.ForeignKey(Book, related_name='reviews')
    reviewer = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
