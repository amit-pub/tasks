# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.shortcuts import render_to_response

from django.http import HttpResponse
from django.template.context import RequestContext


from . import db_data
import json

# Create your views here.
def index(request):
    print request
    mysql = db_data.MySQLDB()
    hello_msg = "\n\n Hello, World. You're at FB-CON.!"
    data = mysql.get_all_data()
    result = {"msg": hello_msg, "data": data}
    return render_to_response("data.html", {"data": data})
    return render('data.html', request, json.dumps(data, indent=4, sort_keys=4))
    return HttpResponse(json.dumps(data, indent=4, sort_keys=True))

def login(request):
    print "Login: %s ---- %s --- " % (request, dir(request))
    return HttpResponse("\n\n At login page!")


def logout(request):
    return HttpResponse("\n\n At logout page!")

    
def home(request):
    d = {'request': request, 'user': request.user}
    context = RequestContext(request,
                           {'request': request,
                            'user': request.user})
    return render(request, 'home.html', d)

