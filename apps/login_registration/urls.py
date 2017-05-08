from django.conf.urls import url
from . import views

app_name = 'login_registration'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login$', views.login, name='login'),
    url(r'^validate$', views.validate, name='validate'),
    url(r'^success$', views.success, name='success')
]
