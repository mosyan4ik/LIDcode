from django.utils import timezone
import re

from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
from django.db import models
from django.contrib.postgres.fields import CITextField
from django.db.models import PositiveIntegerField, ManyToManyField, ForeignKey, EmailField
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
    timeNow = models.DateTimeField(auto_now=True, verbose_name="Время создания")
    results = CITextField(blank=True, null=True, verbose_name="Результаты")
    materials = CITextField(blank=True, null=True, verbose_name="Материалы")
    image = models.ImageField(upload_to="images/%Y/%m/%d/events", verbose_name="Логотип")
    date_register = models.DateTimeField(blank=True, null=True, verbose_name="Дата начала регистрации")
    date_closeRegister = models.DateTimeField(blank=True, null=True, verbose_name="Дата конца регистрации")
    date_start = models.DateTimeField(blank=True, null=True, verbose_name="Дата начала соревнования")
    date_end = models.DateTimeField(blank=True, null=True, verbose_name="Дата конца соревнования")
    additionalMaterial = CITextField(blank=True, null=True, verbose_name="Дополнительные материалы")
    timePublicationAdditionalMaterial = models.DateTimeField(blank=True, null=True,
                                                             verbose_name="Время публикации дополнительных материалов")
    organizers = ManyToManyField("Organizers", blank=True, related_name="my_organizers",
                                 verbose_name='Организаторы')
    sponsors = ManyToManyField("Sponsors", blank=True, related_name="my_sponsors", verbose_name='Спонсоры')

    participants = ManyToManyField("Team", blank=True, related_name="my_participants",
                                   verbose_name='Участвующие команды')

    def getParticipant(self):
        return Team.objects.filter(my_event=self.pk).filter(approvement='approved').count()

    def getrange(self):
        return (range(1, int(str(self.numberofparticipants)) + 1))

    def get_absolute_url(self):
        return reverse('event', kwargs={'event_id': self.pk})

    def get_registration_url(self):
        return reverse('registrations', kwargs={'event_id': self.pk})

    def get_final_registrations_url(self):
        return reverse('final_registrations', kwargs={'event_id': self.pk})

    def now_time_comparison_date_register(self):
        if self.date_register:
            if self.date_register < timezone.now():
                self.status = 'openRegistration'
                self.save()
            else:
                self.status = 'announcement'
                self.save()
            return self.date_register < timezone.now()
        return False

    def now_time_comparison_date_closeRegister(self):
        if self.date_closeRegister:
            if self.date_closeRegister < timezone.now():
                self.status = 'closeRegistration'
                self.save()
            return self.date_closeRegister < timezone.now()
        return False

    def now_time_comparison_date_start(self):
        if self.date_start:
            if self.date_start < timezone.now():
                self.status = 'startCompetition'
                self.save()
            return self.date_start < timezone.now()
        return False

    def now_time_comparison_date_end(self):
        if self.date_end:
            if self.date_end < timezone.now():
                self.status = 'endCompetition'
                self.save()
            return self.date_end < timezone.now()
        return False

    def now_time_comparison_timePublicationAdditionalMaterial(self):
        if self.timePublicationAdditionalMaterial:
            if self.timePublicationAdditionalMaterial < timezone.now():
                self.status = 'publicationExtraMaterials'
                self.save()
            return self.timePublicationAdditionalMaterial < timezone.now()
        return False

    def editLink(self):
        mater = re.split('\r|\n|\t| |\v|\f', str(self.additionalMaterial))
        for i in range(len(mater)):
            if 'http' in mater[i]:
                mater[i] = f'<a href="{mater[i].replace("<br>", "")}">' + mater[i] + "</a>"
        self.additionalMaterial = ' '.join(mater)
        return self.additionalMaterial

    def editLinkMaterial(self):
        mater = re.split('\r|\n|\t| |\v|\f', str(self.materials))
        for i in range(len(mater)):
            if 'http' in mater[i]:
                mater[i] = f'<a href="{mater[i].replace("<br>", "")}">' + mater[i] + "</a>"
        self.materials = ' '.join(mater)
        return self.materials

    def check_registrate(self):
        if self.date_register and self.date_closeRegister:
            return (self.date_register < timezone.now()) and (timezone.now() < self.date_closeRegister)
        return False

    def __str__(self):
        return f'{self.name}'

    class Meta:
        managed = True
        db_table = 'event'
        verbose_name = 'Соревнование'
        verbose_name_plural = 'Соревнования'
        ordering = ['name']


class Organizers(models.Model):
    image = models.ImageField(upload_to="images/%Y/%m/%d/organizers", verbose_name="Логотип")
    name = CITextField(verbose_name="Наименование")
    link = CITextField(verbose_name="Ссылка")

    def __str__(self):
        return f'{self.name}'

    class Meta:
        managed = True
        db_table = 'organizers'
        verbose_name = 'Организатор'
        verbose_name_plural = 'Организаторы'
        ordering = ['name']


class Sponsors(models.Model):
    image = models.ImageField(upload_to="images/%Y/%m/%d/sponsors", verbose_name="Логотип")
    name = CITextField(verbose_name="Наименование")
    link = CITextField(verbose_name="Ссылка")

    def __str__(self):
        return f'{self.name}'

    class Meta:
        managed = True
        db_table = 'sponsors'
        verbose_name = 'Спонсор'
        verbose_name_plural = 'Спонсоры'
        ordering = ['name']


class Team(models.Model):
    answer = (
        ('hold', 'Ожидает'),
        ('rejected', 'Отклонено'),
        ('approved', 'Принято'),
    )

    name = CITextField(verbose_name="Наименование команды")
    teamMembers = ManyToManyField("Participant")
    coach = ForeignKey('Participant',  on_delete=models.PROTECT, related_name='my_coach',
                       verbose_name='Тренер')
    contactPerson = ForeignKey('Participant',  on_delete=models.PROTECT, related_name='my_contactPerson',
                               verbose_name='Контактное лицо')
    approvement = CITextField(null=False, blank=False, default='hold', choices=answer,
                              verbose_name='Статус заявки')
    my_event = ForeignKey('Event', on_delete=models.CASCADE, related_name='my_event',
                          verbose_name='Соревнование')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        managed = True
        db_table = 'team'
        verbose_name = 'Команда'
        verbose_name_plural = 'Команды'
        ordering = ['name']


class Participant(models.Model):
    name = CITextField(verbose_name="ФИО")
    emailadress = EmailField(verbose_name="Электронная почта")
    phonenumber = CITextField(verbose_name="Номер телефона")
    organization = CITextField(verbose_name="Организация")
    university_faculty = CITextField(blank=True, null=True, verbose_name="Факультет")
    university_course = CITextField(blank=True, null=True, verbose_name="Курс")
    iscoach = models.BooleanField(blank=True, null=True, verbose_name="Тренер")
    iscontactFace = models.BooleanField(blank=True, null=True, verbose_name="Контактное лицо")

    def __str__(self):
        return f'{self.name}'

    class Meta:
        managed = True
        db_table = 'participant'
        verbose_name = 'Участник'
        verbose_name_plural = 'Участники'
        ordering = ['name']
