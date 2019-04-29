from django.conf.urls import url
from . import views

urlpatterns = [
    url('login/', views.login, name='login'),
    url('logout/', views.logout, name='logout'),
    url('fb/', views.index, name='index'),
    url('home/', views.home, name='home'),
    #url(r'^$', views.index, name='index'),
]
