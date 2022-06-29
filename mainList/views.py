from django.forms import modelformset_factory
from django.shortcuts import redirect, render
from .forms import *
from .signals import send


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


def registrationForm(request, event_id):
    obj = Event.objects.get(pk=event_id)
    if request.method == "POST":
        form = personalForm(request.POST)
        if form.is_valid():
            lastuser = form.save(commit=False)
            lastuser.save()
            team = Team(name=str(lastuser), contactPerson=lastuser, coach=lastuser)
            team.my_event = obj
            team.save()
            team.teamMembers.add(lastuser)
            team.save()
            send(team.contactPerson.emailadress, obj, 'находится в ожидании')
        return redirect('home')
    else:
        form = personalForm()

    context = {
        'form': form,
        'obj': obj,
    }

    return (
        render(request, 'mainList/registrationsForm.html', context=context)
    )


def registrationEnd(request, event_id):
    obj = Event.objects.get(pk=event_id)
    obj2 = Team()
    if request.method == "POST":
        form = registrationsEnd(request.POST)
        registrationsFormSet = modelformset_factory(Participant, form=registrationsForm, extra=obj.numberofparticipants,
                                                    max_num=obj.numberofparticipants)
        qs = Participant.objects.all().filter(name='')
        formset = registrationsFormSet(request.POST or None, queryset=qs)

        if form.is_valid() and formset.is_valid():
            team = form.save(commit=False)
            team.my_event = obj
            # team.save()
            members = []
            for member_form in formset:
                team_member = member_form.save()
                members.append(team_member)
            for member in members:
                if member.iscoach:
                    team.coach = member
                if member.iscontactFace:
                    team.contactPerson = member
            try:
                str(team.coach)
            except:
                team.coach = member
            try:
                str(team.contactPerson)
            except:
                team.contactPerson = member

            team.save()
            for i in members:
                team.teamMembers.add(i)
            team.save()
            send(team.contactPerson.emailadress, obj, 'находится в ожидании')

            return redirect('home')
    else:
        form = registrationsEnd()
        registrationsFormSet = modelformset_factory(Participant, form=registrationsForm, extra=obj.numberofparticipants,
                                                    max_num=obj.numberofparticipants)
        qs = Participant.objects.all().filter(name='')
        formset = registrationsFormSet(request.POST or None, queryset=qs)

    context = {
        'form': form,
        'formset': formset,
        'obj': obj,
    }

    return (
        render(request, 'mainList/registrationEnd.html', context=context)
    )
