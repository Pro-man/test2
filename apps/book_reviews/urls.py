from django.conf.urls import url
from . import views

app_name = 'books'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<book_id>\d+)$', views.book_details, name='book_details'),
    url(r'^users/(?P<user_id>\d+)$', views.user_details, name='user_details'),
    url(r'^add_review/(?P<book_id>\d+)$', views.add_review, name='add_review'),
    url(r'^delete_review/(?P<book_id>\d+)/(?P<review_id>\d+)$', views.delete_review, name='delete_review'),
    url(r'^add', views.add_form, name='add_form'),
    url(r'^create', views.create_review, name='create_review'),
    url(r'^logout', views.logout, name='logout')
]
