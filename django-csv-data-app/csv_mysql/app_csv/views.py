# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View

from .models import CsvRow
from . import data_mgr


data_manager = data_mgr.DataManager()

def index(request):
    # this is just for the sake of sanity test
    return HttpResponse("this is INDEX page")


class ApiHandler(View):

    def post(self, request):
        # POST request to be blocked. This is just to show
        # to block unsupported APIs
        return HttpResponse(status=405)

    def get(self, request, **kwargs):
        query = dict(request.GET.viewitems())
        data = data_manager.get_data(query)
        return JsonResponse(data, safe=False, json_dumps_params={"indent":4})


def cost_per_install(request):
    # this is a separate method added for calculating CPI separately
    # this method from here on has few or more Hard-coded values/filters
    query = dict(request.GET.viewitems())
    data = data_manager.get_cpi(query)
    return JsonResponse(data, safe=False, json_dumps_params={"indent":4})
