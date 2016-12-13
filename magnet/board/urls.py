from django.conf.urls import url

from . import views

app_name = 'board'

urlpatterns = [
    url(r'^scroll(?P<scroll_x>[0-9]+)-(?P<scroll_y>[0-9]+)$', views.index, name='index'),
    url(r'^$', views.index, name='index'),
    url(r'^reposition$', views.reposition, name='reposition'),
    url(r'^add_or_del_phrase$', views.add_or_del_phrase, name='add_or_del_phrase'),
    url(r'^login/(?P<error_code>[0-9]+)$', views.login_form, name='login_form'),
    url(r'^login$', views.login_form, name='login_form'),
    url(r'^login-(?P<error_code>[0-9]+)$', views.auth_login, name='login'),
    url(r'^logout$', views.auth_logout, name='logout'),
    url(r'^register-(?P<error_code>[0-9]+)$', views.auth_register, name='register')
]
