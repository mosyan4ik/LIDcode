# import time
#
# import self as self
# from django.test import TestCase
# from selenium import webdriver
# from selenium.webdriver import Keys
# # Create your tests here.
# from selenium.webdriver.common.by import By
# import unittest
#
# driver = webdriver.Chrome(
#         executable_path=r'G:\py_Django_proj\courseWork\LIDcodeSite\mainList\chromedriver\chromedriver.exe')
#
# class TestStringMethods(unittest.TestCase):
#     url = 'http://127.0.0.1:8000/'
#     admin = url + 'admin/'
#
#     def test_loginAdmin(self):
#         driver.get(self.admin)
#         # time.sleep(2)
#
#         login_input = driver.find_element(by=By.ID, value='id_username')
#         login_input.clear()
#         login_input.send_keys('admin')
#         # time.sleep(2)
#
#         password_input = driver.find_element(by=By.ID, value='id_password')
#         password_input.clear()
#         password_input.send_keys('admin')
#         # time.sleep(2)
#         password_input.send_keys(Keys.ENTER)
#         # time.sleep(2)
#
#         adminString = driver.find_element(by=By.XPATH, value="//*[@id='user-tools']/strong")
#         self.assertTrue('ADMIN', adminString)
#
#     def test_navigation(self):
#         driver.get(self.url)
#         title_name_list = driver.find_element(by=By.CLASS_NAME, value='main-title')
#         self.assertTrue('Доступные соревнования', title_name_list)
#
#         driver.get(self.url + 'finished')
#         title_name_list = driver.find_element(by=By.CLASS_NAME, value='main-title')
#         self.assertTrue('Завершенные соревнования', title_name_list)
#
#
#
#
#     def test_quit_close(self):
#         driver.close()
#         driver.quit()
#
# if __name__ == '__main__':
#     unittest.main()
#
#
#
