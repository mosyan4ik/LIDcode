import os

from django.test import TestCase

import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LIDcodeSite.LIDcodeSite.settings")
django.setup()
from mainList.forms import *

class FormsPersonalTest(TestCase):

    def test_form(self):
        emailadress = "m321fdsfsasg3124dsadasf24324234324234234543576584gds8gghffgmdsnjfghjfjf5@mail.ru"
        data = {
            'name': 'Игорь',
            'emailadress': emailadress,
            'phonenumber': '89993333564',
            'organization': "РРР"
        }
        form = personalForm(data=data)
        form.is_valid()

        form.save()
        self.assertTrue(Participant.objects.filter(emailadress=emailadress).count() == 1)


class FormsRegistrationsTest(TestCase):

    def test_form(self):
        emailadress = "m321fdsfsasg3124dsadasf24324234324234234543576584gds8gghffgmdsnjfghjfjf5@mail.ru"
        data = {
            'name': 'Игорь',
            'emailadress': emailadress,
            'phonenumber': '89993333564',
            'organization': "РРР"
        }
        form = registrationsForm(data=data)
        form.is_valid()

        form.save()
        self.assertTrue(Participant.objects.filter(emailadress=emailadress).count() == 1)