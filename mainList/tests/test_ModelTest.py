import os
import unittest

from django.conf import settings
from django.db.models import QuerySet
from django.test import TestCase
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LIDcodeSite.LIDcodeSite.settings")
django.setup()
# settings.configure()
from mainList.models import *


class ModelsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.event = Event.objects.create(name='Соревнование',
                                         status='announcement',
                                         numberofparticipants=1,
                                         numberComands=10,
                                         regulations='Правила',
                                         results="Результаты",
                                         materials="Материалы",
                                         image="images/2022/06/27/events/Кубок.jpg",
                                         additionalMaterial='')

        cls.partisipant1 = Participant.objects.create(name='ИванВ',
                                                      emailadress='mosyan25@mail.ru',
                                                      phonenumber='+79209659933',
                                                      organization='М.Видео')

        cls.partisipant2 = Participant.objects.create(name='Артем',
                                                      emailadress='mosyan25@mail.ru',
                                                      phonenumber='+79209667733',
                                                      organization='DNS')

        cls.team = Team.objects.create(name='Одуванчик',
                                       coach=cls.partisipant1,
                                       contactPerson=cls.partisipant2,
                                       my_event=cls.event)

        cls.org = Organizers.objects.create(name="Организатор",
                                            image='images/2022/06/26/organizers/А-Вижн.png',
                                            link="https://sbis.ru/contragents/7604082087/760401001")

        cls.spn = Sponsors.objects.create(name="Спонсор",
                                          image="images/2022/06/26/sponsors/Akvelon.png",
                                          link="https://akvelon.com/")

        cls.team.teamMembers.add(cls.partisipant1)
        cls.team.teamMembers.add(cls.partisipant2)

    def test_Participant(cls):
        cls.assertTrue(cls.partisipant1 in Participant.objects.all())
        cls.assertTrue(cls.partisipant2 in Participant.objects.all())

    def test_Team(cls):
        cls.assertTrue(cls.team in Team.objects.all())

    def test_Event(cls):
        cls.assertTrue(cls.event in Event.objects.all())

    def test_Team_Coach(cls):
        cls.assertTrue(cls.team.coach == cls.partisipant1)

    def test_Team_ContactPerson(cls):
        cls.assertTrue(cls.team.contactPerson == cls.partisipant2)

    def test_Team_event(cls):
        cls.assertTrue(cls.team.my_event == cls.event)

    def test_Event_TeamHold(cls):
        cls.assertFalse(cls.event.participants.contains(cls.team))

    def test_Event_TeamReject(cls):
        cls.team.approvement = 'rejected'
        cls.team.save()
        cls.assertFalse(cls.event.participants.contains(cls.team))

    def test_Event_TeamApprovedReject(cls):
        cls.team.approvement = 'approved'
        cls.team.save()
        cls.team.approvement = 'rejected'
        cls.team.save()
        cls.assertFalse(cls.event.participants.contains(cls.team))

    def test_Event_TeamApproved(cls):
        cls.team.approvement = 'approved'
        cls.team.save()
        cls.assertTrue(cls.event.participants.contains(cls.team))

    def test_Organizers(cls):
        cls.assertTrue(cls.org in Organizers.objects.all())

    def test_Sponsors(cls):
        cls.assertTrue(cls.spn in Sponsors.objects.all())

    def test_Event_Organizers(cls):
        cls.event.organizers.add(cls.org)
        cls.assertTrue(cls.event.organizers.contains(cls.org))

    def test_Event_Sponsors(cls):
        cls.event.sponsors.add(cls.spn)
        cls.assertTrue(cls.event.sponsors.contains(cls.spn))
