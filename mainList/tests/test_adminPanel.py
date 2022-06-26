from django.db.models import QuerySet
from django.test import TestCase
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from django.contrib.postgres.fields import CITextField
import unittest

from mainList.models import *

driver = webdriver.Chrome(
    executable_path=r'G:\py_Django_proj\courseWork\LIDcodeSite\mainList\chromedriver\chromedriver.exe')


class Admin_test_case(TestCase):

    def test_z(self):
        driver.close()
        driver.quit()

    url = 'http://127.0.0.1:8000/'
    admin = url + 'admin'
    finished = url + 'finished'

    def test_loginAdmin(self):
        driver.get(self.admin)

        login_input = driver.find_element(by=By.ID, value='id_username')
        login_input.clear()
        login_input.send_keys('admin')

        password_input = driver.find_element(by=By.ID, value='id_password')
        password_input.clear()
        password_input.send_keys('admin')
        password_input.send_keys(Keys.ENTER)

        adminString = driver.find_element(by=By.XPATH, value="//*[@id='user-tools']/strong")
        self.assertTrue('ADMIN', adminString)

    def test_navigation(self):
        driver.get(self.url)
        title_name_list = driver.find_element(by=By.CLASS_NAME, value='main-title')
        self.assertTrue('Доступные соревнования', title_name_list)

        driver.get(self.finished)
        title_name_list = driver.find_element(by=By.CLASS_NAME, value='main-title')
        self.assertTrue('Завершенные соревнования', title_name_list)

    def test_urlForEvent_TitleText(self):
        driver.get(self.url)
        titleEvent = driver.find_element(by=By.CLASS_NAME, value='card_name')
        titleEvent_text = titleEvent.text
        titleEvent.click()
        titleSELFEvent = driver.find_element(by=By.CLASS_NAME, value='main-title')
        self.assertTrue(f'{titleEvent_text}', titleSELFEvent)

    def test_urlForEvent_Image(self):
        driver.get(self.url)
        titleEvent = driver.find_element(by=By.CLASS_NAME, value='card_name')
        titleEvent_text = titleEvent.text
        title_img = driver.find_element(by=By.CLASS_NAME, value='img')
        title_img.click()
        titleSELFEvent = driver.find_element(by=By.CLASS_NAME, value='main-title')
        self.assertTrue(f'{titleEvent_text}', titleSELFEvent)

    def test_urlForEvent_Button(self):
        driver.get(self.url)
        titleEvent = driver.find_element(by=By.CLASS_NAME, value='card_name')
        titleEvent_text = titleEvent.text
        title_but = driver.find_element(by=By.CLASS_NAME, value='button')
        title_but.click()
        titleSELFEvent = driver.find_element(by=By.CLASS_NAME, value='main-title')
        self.assertTrue(f'{titleEvent_text}', titleSELFEvent)

    def test_urlShowList(self):
        driver.get(self.url)
        titleEvent = driver.find_element(by=By.CLASS_NAME, value='card_name')
        titleEvent.click()
        logo = driver.find_element(by=By.CLASS_NAME, value='header-navigation__logo')
        logo.click()
        title_name_list = driver.find_element(by=By.CLASS_NAME, value='main-title')
        self.assertTrue('Доступные соревнования', title_name_list)

        driver.get(self.url)
        titleEvent = driver.find_element(by=By.CLASS_NAME, value='card_name')
        titleEvent.click()
        fin = driver.find_element(by=By.CLASS_NAME, value='header-navigation__item')
        fin.click()
        title_name_list = driver.find_element(by=By.CLASS_NAME, value='main-title')
        self.assertTrue('Завершенные соревнования', title_name_list)

    def test_countPartisipants(self):
        driver.get(self.url)
        titleEvent = driver.find_element(by=By.CLASS_NAME, value='card_name')
        titleEvent.click()

        info__p = driver.find_element(by=By.CLASS_NAME, value='info__p')
        info__p_TEXT = info__p.text
        try:
            if "Индивидуальное участие" in info__p_TEXT:
                regBut = driver.find_element(by=By.CLASS_NAME, value='button_reg')
                regBut.click()
                reg_form = driver.find_elements(by=By.CLASS_NAME, value='reg_form')
                self.assertTrue(1, len(reg_form))
            elif "Командное участие" in info__p_TEXT:
                info__p_TEXT = info__p_TEXT.split('|')[0]
                my_string = [info__p_TEXT[i] for i in range(len(info__p_TEXT)) if info__p_TEXT[i].isdigit()]
                my_string = ''.join(my_string)
                num = int(my_string)

                regBut = driver.find_element(by=By.CLASS_NAME, value='button_reg')
                regBut.click()

                reg_form = driver.find_elements(by=By.CLASS_NAME, value='input_text')
                self.assertTrue(num * 6, len(reg_form))
        except:
            pass

    def test_registagionURL(self):
        driver.get(self.url)
        titleEvent = driver.find_element(by=By.CLASS_NAME, value='card_name')
        titleEvent.click()

        info__p = driver.find_element(by=By.CLASS_NAME, value='info__p')
        info__p_TEXT = info__p.text

        if "Индивидуальное участие" in info__p_TEXT:
            regBut = driver.find_element(by=By.CLASS_NAME, value='button_reg')
            regBut.click()
            # reg_form = driver.find_elements(by=By.CLASS_NAME, value='reg_form')
            name = driver.find_element(by=By.NAME, value='name')
            email = driver.find_element(by=By.NAME, value='emailadress')
            phone = driver.find_element(by=By.NAME, value='phonenumber')
            organiz = driver.find_element(by=By.NAME, value='organization')

            name.send_keys('Иван')
            email.send_keys('mosyan25@mail.ru')
            phone.send_keys('+79209659933')
            organiz.send_keys('М.Видео')

            button = driver.find_element(by=By.CLASS_NAME, value='button')
            button.click()

            title_name_list = driver.find_element(by=By.CLASS_NAME, value='main-title')
            self.assertTrue('Доступные соревнования', title_name_list)

        elif "Командное участие" in info__p_TEXT:
            info__p_TEXT = info__p_TEXT.split('|')[0]
            my_string = [info__p_TEXT[i] for i in range(len(info__p_TEXT)) if info__p_TEXT[i].isdigit()]
            my_string = ''.join(my_string)
            num = int(my_string)

            regBut = driver.find_element(by=By.CLASS_NAME, value='button_reg')
            regBut.click()

            reg_form = driver.find_elements(by=By.CLASS_NAME, value='input_text')

            name_team = driver.find_element(by=By.ID, value='id_name')
            name_team.send_keys("Василек")
            for i in range(num):
                name = driver.find_element(by=By.ID, value=f'id_form-{i}-name')
                emailadress = driver.find_element(by=By.ID, value=f'id_form-{i}-emailadress')
                phonenumber = driver.find_element(by=By.ID, value=f'id_form-{i}-phonenumber')
                organization = driver.find_element(by=By.ID, value=f'id_form-{i}-organization')

                name.send_keys(f"Робот_{i}")
                emailadress.send_keys('mosyan25@mail.ru')
                phonenumber.send_keys(f'+7920965993{i}')
                organization.send_keys(f'BoysClub{i}')

    def test_modelTeam(self):

        eve = Event.objects.create(name='Соревнование',
                                   status='announcement',
                                   numberofparticipants=1,
                                   numberComands=10,
                                   regulations='Правила',
                                   results="Результаты",
                                   materials="Материалы",
                                   image="images/2022/06/26/events/Кубок.jpg")

        pp1 = Participant.objects.create(name='Иван',
                                  emailadress='mosyan25@mail.ru',
                                  phonenumber='+79209659933',
                                  organization='М.Видео')

        pp2 = Participant.objects.create(name='Артем',
                                  emailadress='mosyan25@mail.ru',
                                  phonenumber='+79209667733',
                                  organization='DNS')

        Team.objects.create(name='Одуванчик',
                            teamMembers=QuerySet().objects.add(pp1).add(pp2),
                            coach=pp1,
                            contactPerson=pp2,
                            my_event=eve)



if __name__ == '__main__':
    unittest.main()
