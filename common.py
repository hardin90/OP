from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import quote
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException
from time import sleep

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.base_url = "https://%s:%s@%s/Admin"

    def find_element(self, xpath, time=10):
        return WebDriverWait(self.driver, time).until(EC.presence_of_element_located((By.XPATH, xpath)),
                                                      message=f"Can't find element by locator {xpath}")

    def find_elements(self, xpath, time=10):
        return WebDriverWait(self.driver, time).until(EC.presence_of_all_elements_located((By.XPATH, xpath)),
                                                      message=f"Can't find elements by locator {xpath}")

    def click(self, element):
        try:
            for _ in range(5):
                try:
                    element.click()
                    break
                except ElementClickInterceptedException:
                    sleep(1)

        except Exception as e:
            print(e, type(e))

    def get_att(self, xpath, name_attribute):
        value = self.find_element(xpath).get_attribute(name_attribute)
        return value

    def execute_script(self, query):
        return self.driver.execute_script("return %s" % query)

    def login(self, username, password, host):
        return self.driver.get(self.base_url % (quote(username), quote(password), host))







# import logging
# import os
# import shutil
# import subprocess
# import yaml
# import paramiko
# import argparse
#
# from contextlib import contextmanager
# from functools import wraps
# from sys import exit
# from selenium import webdriver
# from selenium.common.exceptions import NoSuchElementException, \
#     ElementClickInterceptedException, ElementNotInteractableException, StaleElementReferenceException
# from selenium.webdriver.support import expected_conditions
# from time import sleep, monotonic
# from xvfbwrapper import Xvfb
# from selenium.webdriver.common.action_chains import ActionChains
# import psycopg2
# from datetime import datetime
#
#
# LOGGING_FORMAT = "%(asctime)s [%(name)s] %(levelname)s: %(message)s"
# LOG = logging.getLogger()
# cred_path = '/etc/openstack/cred'
#
# def check_existence(tester, msg, err_msg, xpath=None, id=None, name=None,
#                     class_name=None):
#
#     if tester.exists(xpath=xpath, id=id, name=name,
#                      class_name=class_name):
#         LOG.info(msg)
#     else:
#         raise Exception(err_msg)
#
# def getPassword(host, ssh_user, ssh_pass):
#     '''
#     Функция получает пароль из файла cred хранящимся на контроллере
#     путь к файлу задается в перменной cred_path
#     обычно это /etc/openstack/cred или /home/rustack/cred
#     '''
#     LOG.info('Получение пароля АЗ для WEB интерфейса')
#
#     client = paramiko.SSHClient()
#     client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#     client.connect(hostname=host, username=ssh_user, password=ssh_pass, port=22)
#     stdin, stdout, stderr = client.exec_command('cat %s | grep PASSWORD' % cred_path)
#     data = stdout.read() + stderr.read()
#     client.close()
#     web_pass=data.decode('utf-8').split('=')[1]
#     LOG.info('Получен пароль АЗ : %s' % web_pass)
#     return web_pass
#
# def get_params_from_host_yml(host,ssh_user,ssh_pass, param):
#     LOG.info('Получение пароля АЗ для WEB интерфейса')
#
#     client = paramiko.SSHClient()
#     client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#     client.connect(hostname=host, username=ssh_user, password=ssh_pass, port=22)
#     path='/var/lib/rustack-ansible/group_vars/all/user_vars.yml'
#     stdin, stdout, stderr = client.exec_command('cat %s | grep %s:' % (path, param))
#     data = stdout.read() + stderr.read()
#     client.close()
#     print(data.decode('utf-8'))
#     response = data.decode('utf-8')
#     LOG.info('Получен %s' % (response))
#     return response
#
#
#
# def get_args():
#     """
#     Получение агрументов host, ssh_user и ssh_pass при запуске теста
#     агрументы указываются после имени файла теста
#     пример
#     python testNNN.py <host> <user> <password>
#     """
#     parser = argparse.ArgumentParser()
#     parser.add_argument('host', type=str,
#                         help = "адрес web интерфеса портала")
#     parser.add_argument('ssh_user', type=str,
#                         help = "логин для ssh к серверу")
#     parser.add_argument('ssh_pass', type=str,
#                         help="пароль для ssh к серверу портала")
#     """    parser.add_argument('thread', type=str,
#                         help="number of thread")"""
#     args = parser.parse_args()
#     host = args.host
#     ssh_user = args.ssh_user
#     ssh_pass = args.ssh_pass
#     """thread=args.thread"""
#     return host, ssh_user, ssh_pass
#
# def init(test_name):
#     logging.basicConfig(level=logging.INFO, format=LOGGING_FORMAT)
#
#     global LOG
#     LOG = logging.getLogger(test_name)
#     LOG.info("Инициализация теста")
#     selenium_logger = logging.getLogger(
#         "selenium.webdriver.remote.remote_connection")
#     selenium_logger.setLevel(logging.INFO)
#
# def _sleep_after(default_wait=0):
#     def internal(f):
#         @wraps(f)
#         def wrapper(*args, **kwargs):
#             if 'wait' in kwargs:
#                 wait = kwargs['wait']
#                 kwargs.delete('wait')
#             else:
#                 wait = default_wait
#             result = f(*args, **kwargs)
#             sleep(wait)
#             return result
#         return wrapper
#     return internal
#
# def _try_find_element(timeout=15, multiple=False, raise_on_fail=False):
#     def internal(f):
#         @wraps(f)
#         def wrapper(*args, **kwargs):
#             find_constrains = ('xpath', 'id', 'name', 'class_name')
#             find_params = {k: v for k, v in kwargs.items()
#                             if k in find_constrains}
#             func_params = {k: v for k, v in kwargs.items()
#                            if k not in find_constrains}
#             if find_params:
#                 find_func = getattr(args[0], '_finds' if multiple else '_find')  # args[0] - self
#                 stop_time = monotonic() + timeout
#                 while stop_time > monotonic():
#                     element = find_func(**find_params)
#                     func_params['element'] = element
#                     if (element is not None) and (element != []):
#                         #print(**find_params)
#                         break
#                 else:
#                     if raise_on_fail:
#                         raise Exception('Element not found "%s", timeout=%s' % (find_params, timeout))
#             return f(*args, **func_params)
#         return wrapper
#     return internal
#
# def create_table(t_name):
#     with psycopg2.connect(dbname='reports', user='postgres',
#                           password='qweqwe12q', host='localhost') as con:
#         cur = con.cursor()
#
#         query = """
#         CREATE TABLE %s (
#             users VARCHAR(255),
#             browser VARCHAR(255),
#             test VARCHAR(255),
#             status VARCHAR(255),
#             error VARCHAR(255)
#         )
#         """ % t_name
#         cur.execute(query)
#         con.commit()
#
#
# def to_bd(data, user, browser='FireFox', test=None, status=None, error=None):
#     with psycopg2.connect(dbname='reports', user='postgres',
#                           password='qweqwe12q', host='localhost') as con:
#         cur = con.cursor()
#         query = "INSERT INTO report (data, users, browser, test, status, error) VALUES (%s, %s, %s, %s, %s, %s)"
#         record = (data, user, browser,  test, status, error)
#         cur.execute(query, record)
#         con.commit()
#
# now = datetime.now().strftime("%D %H:%M:%S")
#
# @contextmanager
# def test_wrapper(test_name):
#     init(test_name)
#     test, user = test_name.split(' ', 3)[:2]
#     #now = datetime.now().strftime("%D %H:%M:%S")
#     # create_table(t_name)
#     try:
#         yield
#     except Exception as e:
#         LOG.error(str(e))
#         to_bd(data=now, user=user, test=test, status='Fail', error=(str(type(e))+str(e)))
#         exit(1)
#     else:
#         LOG.info("Тест успешно пройден!")
#         #to_bd(user, test, 'Success')
#         to_bd(data=now, user=user, test=test, status='Success', error='Not Error')
#
#
# class Tester(object):
#     """
#     Методы объекта:
#         .navigate(url)
#         .click(element, wait=True)
#         ,context_click(element)
#         .doubleclick(element)
#         .input(element, text)
#         .clear(element)
#         .exists(element, wait=False)
#         .get_text(element)
#         .GetExtjsId(req)
#         .close()
#
#     """
#
#     def __init__(self):
#         # capabilities = {
#         #     "browserName": "chrome",
#         #     "version": "77.0",
#         #     "enableVNC": True,
#         #     "enableVideo": False
#         # }
#
#         # capabilities = {
#         #     "browserName": "opera",
#         #     "version": "63.0",
#         #     "enableVNC": True,
#         #     "enableVideo": False
#         # }
#
#
#         # self.driver = webdriver.Remote(
#         #     command_executor="http://10.11.3.90:4444/wd/hub",
#         #     desired_capabilities=capabilities)
#         self.driver = webdriver.Firefox()
#         self.driver.maximize_window()
#         #self.params = {}
#
#     def _find(self, xpath=None, id=None, name=None, class_name=None):
#         try:
#             if xpath is not None:
#                 el = self.driver.find_element_by_xpath(xpath)
#                 if (el.is_displayed() is False) or (el.is_enabled() is False):
#                     return None
#                 else:
#                     print(xpath)
#                     return el
#             elif id is not None:
#                 el = self.driver.find_element_by_id(id)
#                 if (el.is_displayed() is False) or (el.is_enabled() is False):
#                     return None
#                 else:
#                     return el
#             elif name is not None:
#                 el = self.driver.find_element_by_name(name)
#                 if (el.is_displayed() is False) or (el.is_enabled() is False):
#                     return None
#                 else:
#                     return el
#             elif class_name is not None:
#                 el = self.driver.find_element_by_class_name(class_name)
#                 if (el.is_displayed() is False) or (el.is_enabled() is False):
#                     return None
#                 else:
#                     return el
#             else:
#                 return None
#         except NoSuchElementException:
#             return None
#
#     def _finds(self, xpath=None, id=None, name=None, class_name=None):
#         try:
#             if xpath is not None:
#                 els = self.driver.find_elements_by_xpath(xpath)
#                 for el in els:
#                     if (el.is_displayed() is False) or (el.is_enabled() is False):
#                         return None
#                 return None if els==[] else els
#             elif id is not None:
#                 els = self.driver.find_elements_by_id(id)
#                 for el in els:
#                     if (el.is_displayed() is False) or (el.is_enabled() is False):
#                         return None
#                 return None if els==[] else els
#             elif name is not None:
#                 els = self.driver.find_elements_by_name(name)
#                 for el in els:
#                     if (el.is_displayed() is False) or (el.is_enabled() is False):
#                         return None
#                 return None if els==[] else els
#             elif class_name is not None:
#                 els = self.driver.find_elements_by_class_name(class_name)
#                 for el in els:
#                     if (el.is_displayed() is False) or (el.is_enabled() is False):
#                         return None
#                 return None if els==[] else els
#             else:
#                 return None
#         except NoSuchElementException:
#             return None
#
#     @_sleep_after(default_wait=1)
#     def navigate(self, url):
#         """
#         Переход на страницу
#         Доступные параметры:
#         url - url перехода
#         wait - время ожидания после перехода в сек (по умолчанию 5 сек.)
#         """
#         print('------------------------')
#         print('NAVIGATION %s' % url+' ---------')
#         print('------------------------')
#         self.driver.get(url)
#
#     @_try_find_element(raise_on_fail=True)
#     def click(self, element):
#         """
#         Имитация нажатия мышки
#         Доступные параметры:
#         xpath - xpath HTML объекта
#         id - id HTML объекта
#         name - имя HTML объекта
#         class_name - имя класса HTML объекта
#         element - непосредствнно объект (возвращаемый find_element_by_*)
#         !!! учитывается только один параметр (в вышеперечисленном приоритете)
#         wait - время ожидания после перехода в сек (по умолчанию 5 сек.)
#         """
#         for _ in range(60):
#             try:
#                 element.click()
#                 break
#             except (ElementClickInterceptedException, ElementNotInteractableException, StaleElementReferenceException):
#                 print('Next try...')
#                 sleep(1)
#         else:
#             raise Exception("Could't click")
#
#
#     @_sleep_after(default_wait=5)
#     @_try_find_element()
#     def context_click(self, element, msg=None):
#         """
#         Имитация нажатия мышки
#         Доступные параметры:
#         xpath - xpath HTML объекта
#         id - id HTML объекта
#         name - имя HTML объекта
#         class_name - имя класса HTML объекта
#         element - непосредствнно объект (возвращаемый find_element_by_*)
#         !!! учитывается только один параметр (в вышеперечисленном приоритете)
#         wait - время ожидания после перехода в сек (по умолчанию 5 сек.)
#         """
#         action = ActionChains(self.driver)
#         action.context_click(element)
#         action.perform()
#         if msg:
#             LOG.info(msg)
#
#     @_try_find_element()
#     def doubleclick(self, element, msg=None):
#         """
#         Имитация двойного нажатия мышки
#         Доступные параметры:
#         xpath - xpath HTML объекта
#         id - id HTML объекта
#         name - имя HTML объекта
#         class_name - имя класса HTML объекта
#         element - непосредствнно объект (возвращаемый find_element_by_*)
#         !!! учитывается только один параметр (в вышеперечисленном приоритете)
#         wait - время ожидания после перехода в сек (по умолчанию 5 сек.)
#         """
#         action = ActionChains(self.driver)
#         action.double_click(element)
#         action.perform()
#         if msg:
#             LOG.info(msg)
#
#     @_sleep_after()
#     @_try_find_element()
#     def input(self, element, text, msg=None):
#         """
#         Ввод текста в текстовые поля
#         Доступные параметры:
#         xpath - xpath HTML объекта
#         id - id HTML объекта
#         name - имя HTML объекта
#         class_name - имя класса HTML объекта
#         element - непосредствнно объект (возвращаемый find_element_by_*)
#         !!! учитывается только один параметр (в вышеперечисленном приоритете)
#         text - строка для ввода
#         wait - время ожидания после перехода в сек (по умолчанию 1 сек.)
#         """
#         #Tester.exists(self, element, wait=True)
#         element.send_keys(text)
#         if msg:
#             LOG.info(msg.format(text))
#
#     @_sleep_after()
#     @_try_find_element()
#     def clear(self, element):
#         """
#         Очищает поле ввода
#         Доступные параметры:
#         xpath - xpath HTML объекта
#         id - id HTML объекта
#         name - имя HTML объекта
#         class_name - имя класса HTML объекта
#         element - непосредствнно объект (возвращаемый find_element_by_*)
#         !!! учитывается только один параметр (в вышеперечисленном приоритете)
#         wait - время ожидания после очистки в сек (по умолчанию 1 сек.)
#         """
#         element.clear()
#
#     @_try_find_element()
#     def exists(self, element):
#         """
#         Проверяет наличие элемента
#         Доступные параметры:
#         xpath - xpath HTML объекта
#         id - id HTML объекта
#         name - имя HTML объекта
#         class_name - имя класса HTML объекта
#         element - непосредствнно объект (возвращаемый find_element_by_*)
#         !!! учитывается только один параметр (в вышеперечисленном приоритете)
#         """
#         return element is not None
#
#
#     def exists_now(self, xpath=None, id=None, name=None):
#         element = self._find(xpath=xpath, id=id, name=name)
#         return element is not None
#
#
#     @_try_find_element()
#     def get_text(self, element):
#         """
#         Возвращает текст элемента
#
#         Доступные параметры:
#         xpath - xpath HTML объекта
#         id - id HTML объекта
#         name - имя HTML объекта
#         class_name - имя класса HTML объекта
#         element - непосредствнно объект (возвращаемый find_element_by_*)
#         !!! учитывается только один параметр (в вышеперечисленном приоритете)
#         """
#
#         return str(element.text)
#
#     @_try_find_element(multiple=True)
#     def get_texts(self, element):
#         resp = []
#         for e in element:
#             resp.append(e.text)
#         return resp
#
#
#     def get_screenshot(self, filename):
#         self.driver.get_screenshot_as_file('%s.png' % filename)
#
#
#     @_try_find_element()
#     def size(self, element):
#         return element.size
#
#     @_try_find_element()
#     def location(self, element):
#         return element.location
#
#     def get_screenshot_as_png(self):
#         return self.driver.get_screenshot_as_png()
#
#
#
#     def GetExtjsId(self, req):
#         """
#         Выдает id элемента на основании запроса
#         """
#         print("return Ext.query{}".format(req))
#         resp = self.driver.execute_script("return Ext.query{}".format(req))
#         return resp
#
#     @_try_find_element(multiple=True)
#     def get_elements(self, element):
#         return element
#
#     def send_keys(self, xpath, text):
#         el = self.driver.find_element_by_xpath(xpath)
#         el.send_keys(text)
#
#     def sleep(self, time):
#         # print('Sleep %s' % time)
#         sleep(time)
#
#     def get_cookies(self):
#         return self.driver.get_cookies()
#
#
#     def get_attribute(self, get=None, xpath=None):
#         try:
#             if get is not None:
#                 elem = self._find(xpath=xpath)
#                 return elem.get_attribute(get)
#
#         except Exception as e:
#             LOG.error(e, type(e))
#
#     def swith_to(self, frame):
#         self.driver.switch_to.frame(frame)
#
#
#     def close(self):
#         """ Закрывает браузер """
#         self.driver.close()
#
# class YAMLobj(dict):
#     """
#     Класс работы функции AdminPortal()
#     """
#     def __init__(self, args):
#         super(YAMLobj, self).__init__(args)
#         if isinstance(args, dict):
#             for k, v in args.items():
#                 if not isinstance(v, dict):
#                     try:
#                         self[k] = v.decode('utf-8')
#                     except:
#                         self[k] = v
#                 else:
#                     self.__setattr__(k, YAMLobj(v))
#
#     def __getattr__(self, attr):
#         return self.get(attr)
#
#     def __setattr__(self, key, value):
#         self.__setitem__(key, value)
#
#     def __setitem__(self, key, value):
#         super(YAMLobj, self).__setitem__(key, value)
#         self.__dict__.update({key: value})
#
#     def __delattr__(self, item):
#         self.__delitem__(item)
#
#     def __delitem__(self, key):
#         super(YAMLobj, self).__delitem__(key)
#         del self.__dict__[key]
#
#     def __add__(self, key):
#         return str(key)
#
#
# def AdminPortal(yamlfile="Portal.yaml"):
#     """
#     Преобразовывает .yaml файл, передаваемый функции AdminPortal() в класс
#     В результате можно вызывать содержимое значений yaml фйла,
#         вызывая переменные yaml файла, как методы AdminPortal
#     Например:
#         common.AdminPortal().Portal.menu.button.xpath
#     """
#     try:
#         dict_result = yaml.load(open(yamlfile), Loader=yaml.FullLoader)
#         result = YAMLobj(dict_result)
#         return result
#     except Exception as e:
#         LOG.error(e)
#         raise Exception("Тест не пройден")
#
