from django.db.models.signals import pre_delete, post_delete
from django.dispatch import receiver
from django.utils import timezone
import datetime
import re

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

# Create your models here.
from django.db import models
from django.contrib.postgres.fields import CITextField
from django.db.models import IntegerField, PositiveIntegerField, ManyToManyField, ForeignKey
from django.urls import reverse


class Event(models.Model):
    statusChoise = (
        ('hidden', 'Скрыто'),
        ('announcement', 'Объявление'),
        ('openRegistration', 'Открытие регистрации на соревнование'),
        ('closeRegistration', 'Закрытие регистрации на соревнование'),
        ('startCompetition', 'Соревнование началось'),
        ('endCompetition', 'Соревнование завершилось'),
        ('publicationExtraMaterials', 'Публикация дополнительных материалов'),
        ('processingMaterials', 'Обработка материалов'),
        ('inArchive', 'В архиве')
    )
    viw = ['hidden', 'endCompetition', 'processingMaterials', 'inArchive']
    validatorNumberofparticipants = [
        MinValueValidator(1),
        MaxValueValidator(1000)
    ]

    name = CITextField(verbose_name='Наименование')
    status = CITextField(verbose_name='Статус', choices=statusChoise)
    description = CITextField(blank=True, null=True, verbose_name='Описание')
    numberofparticipants = PositiveIntegerField(verbose_name='Кол-во участников в команде',
                                                validators=validatorNumberofparticipants)
    numberComands = PositiveIntegerField(null=False, verbose_name='Кол-во команд',
                                         validators=validatorNumberofparticipants)
    regulations = CITextField(verbose_name='Правила')
    timeNow = models.DateTimeField(auto_now=True)
    results = CITextField(blank=True, null=True, verbose_name="Результаты")
    materials = CITextField(blank=True, null=True, verbose_name="Материалы")
    image = models.ImageField(upload_to="images/%Y/%m/%d/events", verbose_name="Логотип")
    date_register = models.DateTimeField(blank=True, verbose_name="Дата начала регистрации")
    date_closeRegister = models.DateTimeField(blank=True, verbose_name="Дата конца регистрации")
    date_start = models.DateTimeField(blank=True, verbose_name="Дата начала соревнования")
    date_end = models.DateTimeField(blank=True, verbose_name="Дата конца соревнования")
    additionalMaterial = CITextField(blank=True, null=True, verbose_name="Дополнительные материалы")
    timePublicationAdditionalMaterial = models.DateTimeField(blank=True, null=True,
                                                             verbose_name="Время публикации дополнительных материалов")
    organizers = ManyToManyField("Organizers", blank=True,  related_name="my_organizers",
                                 verbose_name='Организаторы')
    sponsors = ManyToManyField("Sponsors", blank=True,  related_name="my_sponsors", verbose_name='Спонсоры')

    def get_absolute_url(self):
        return reverse('event', kwargs={'event_id': self.pk})


    def now_time_comparison_date_register(self):
        if self.date_register:
            return self.date_register < timezone.now()
        return False

    def now_time_comparison_date_closeRegister(self):
        if self.date_closeRegister:
            return self.date_closeRegister < timezone.now()
        return False

    def now_time_comparison_date_start(self):
        if self.date_start:
            return self.date_start < timezone.now()
        return False

    def now_time_comparison_date_end(self):
        if self.date_end:
            return self.date_end < timezone.now()
        return False

    def now_time_comparison_timePublicationAdditionalMaterial(self):
        if self.timePublicationAdditionalMaterial:
            return self.timePublicationAdditionalMaterial < timezone.now()
        return False

    def editLink(self):
        mater = re.split('\r|\n|\t| |\v|\f', str(self.additionalMaterial))
        for i in range(len(mater)):
            if 'http' in mater[i]:
                mater[i] = f'<a href="{mater[i].replace("<br>", "")}">' + mater[i] + "</a>"
        self.additionalMaterial = ' '.join(mater)
        return self.additionalMaterial

    def check_registrate(self):
        if self.date_register and self.date_closeRegister:
            return (self.date_register < timezone.now()) and (timezone.now() < self.date_closeRegister)
        return False

    class Meta:
        managed = False
        db_table = 'event'
        verbose_name = 'Соревнование'
        verbose_name_plural = 'Соревнования'
        ordering = ['name']


@receiver(pre_delete, sender=Event)
def Event_delete(sender, instance, **kwargs):
    instance.image.delete(False)


class Organizers(models.Model):
    image = models.ImageField(upload_to="images/%Y/%m/%d/organizers", verbose_name="Логотип")
    name = CITextField(verbose_name="Наименование")
    link = CITextField(verbose_name="Ссылка")

    def __str__(self):
        return f'{self.name}'

    class Meta:
        managed = False
        db_table = 'organizers'
        verbose_name = 'Организатор'
        verbose_name_plural = 'Организаторы'
        ordering = ['name']


@receiver(pre_delete, sender=Organizers)
def Organizers_delete(sender, instance, **kwargs):
    instance.image.delete(False)


class Sponsors(models.Model):
    image = models.ImageField(upload_to="images/%Y/%m/%d/sponsors", verbose_name="Логотип")
    name = CITextField(verbose_name="Наименование")
    link = CITextField(verbose_name="Ссылка")

    def __str__(self):
        return f'{self.name}'

    class Meta:
        managed = False
        db_table = 'sponsors'
        verbose_name = 'Спонсор'
        verbose_name_plural = 'Спонсоры'
        ordering = ['name']

@receiver(pre_delete, sender=Sponsors)
def Sponsors_delete(sender, instance, **kwargs):
    instance.image.delete(False)

class Team(models.Model):
    name = CITextField(verbose_name="Наименование команды")
    teamMembers = ManyToManyField("Participant")
    coach = ForeignKey("Participant", on_delete=models.PROTECT, default=1, related_name="my_coach")
    contactPerson = ForeignKey("Participant", on_delete=models.PROTECT, default=1, related_name="my_contactPerson")

class Participant(models.Model):
    name = CITextField(verbose_name="ФИО")
    emailadress = CITextField(verbose_name="Электронная почта")
    phonenumber = CITextField(verbose_name="Номер телефона")
    organization = CITextField(verbose_name="Организация")
    university = CITextField(blank=True, null=True, verbose_name="Университет")
    university_faculty = CITextField(blank=True, null=True, verbose_name="Факультет")
    university_course = CITextField(blank=True, null=True, verbose_name="Курс")
