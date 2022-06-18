from django.db import models

# Create your models here.
from django.db import models
from django.contrib.postgres.fields import IntegerRangeField, CITextField
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

    name = CITextField(verbose_name='Наименование')
    status = CITextField(verbose_name='Статус', choices=statusChoise)
    description = CITextField(blank=True, null=True, verbose_name='Описание')
    numberofparticipants = IntegerRangeField(blank=True, null=True, verbose_name='Кол-во участников')
    regulations = CITextField(verbose_name='Правила')
    timetable = CITextField(verbose_name="Расписание")
    results = CITextField(blank=True, null=True, verbose_name="Результаты")
    materials = CITextField(blank=True, null=True, verbose_name="Материалы")

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_id': self.pk})

    class Meta:
        managed = False
        db_table = ' event'
        verbose_name = 'Соревнование'
        verbose_name_plural = 'Соревнования'
        ordering = ['timetable', 'name']

class Organizers(models.Model):
    image = models.ImageField(upload_to="images/%Y/%m/%d/", verbose_name="Логотип")
    name = CITextField(verbose_name="Наименование")
    link = CITextField(verbose_name="Ссылка")

    class Meta:
        managed = False
        db_table = 'organizers'
        verbose_name = 'Организатор'
        verbose_name_plural = 'Организаторы'
        ordering = ['name']

class Sponsors(models.Model):
    image = models.ImageField(upload_to="images/%Y/%m/%d/", verbose_name="Логотип")
    name = CITextField(verbose_name="Наименование")
    link = CITextField(verbose_name="Ссылка")

    class Meta:
        managed = False
        db_table = 'sponsors'
        verbose_name = 'Спонсор'
        verbose_name_plural = 'Спонсоры'
        ordering = ['name']
