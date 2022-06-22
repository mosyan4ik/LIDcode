from datetime import datetime

from django.shortcuts import render
from django.http import HttpResponse
from .models import *

def index(request):
    data = Event.objects.all()
    viw = ['inArchive', 'hidden', 'endCompetition', 'processingMaterials']
    context = {
        'title': 'Доступные соревнования',
        'dat': data,
        'viw': viw
    }
    return (
        render(request, 'mainList/index.html', context=context)
    )

def finished(request):
    data = Event.objects.all()
    viw = ['inArchive', 'endCompetition', 'processingMaterials']
    context = {
        'title': 'Завершенные соревнования',
        'dat': data,
        'viw': viw
    }
    return (
        render(request, 'mainList/finished.html', context=context)
    )

def show_event(request, event_id):
    obj = Event.objects.get(pk=event_id)

    context = {
        'obj': obj,
    }
    return (
        render(request, 'mainList/show_event.html', context=context)
    )