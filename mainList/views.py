from datetime import datetime

from django.db.models import QuerySet
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import *

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

class Lamoda():
    img = [
        # 'name.png',
        # 'emailadress.png',
        # 'phonenumber.png',
        # 'organization.png',
        # 'university_faculty.png',
        # 'university_course.png',
        0,
        1,
        2,
        3,
        4,
        5,
    ]
    count = 0

    def get_me(self):
        ob = self.img[self.count]
        self.count += 1
        return ob

def registrationForm(request, event_id):
    if request.method == "POST":
        form = registrationsForm(request.POST)
        if form.is_valid():
            form.save()
            human = Participant(form.fields)
            try:
                team = Team.objects.create(pk=(Team.objects.order_by("pk").last().id+1), name=form.fields['name'],
                                           coach=Participant(form.fields),
                                       contactPerson=Participant(form.fields))
            except:
                team = Team.objects.create(id=int(1), name=form.fields['name'], coach=Participant(form.fields),
                                       contactPerson=form.fields['id'])
            team.teamMembers.add(Participant(form.fields))

            team.save()
            return redirect('home')
    else:
        form = registrationsForm()

    obj = Event.objects.get(pk=event_id)



    context = {
        'form': form,
        'obj': obj,

    }

    return (
        render(request, 'mainList/registrationsForm.html', context=context)
    )