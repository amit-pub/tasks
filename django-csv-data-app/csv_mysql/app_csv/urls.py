from django.conf.urls import url
from . import views

urlpatterns = [
    url('api/', views.ApiHandler.as_view(), name='api_handler'),
    url('cpi/', views.cost_per_install, name='cpi'),
    url('/', views.index, name='index'),
]
