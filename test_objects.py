from page_objects import Buttons
from time import sleep

from selenium import webdriver

username = 'admin'
password = 'g15FPPKf'
host = '10.11.3.80'

def test_yandex_search(browser):
    button = Buttons(browser)
    button.login(username, password, host)
    #sleep(5)
    button.filter('Диски')
    button.filter('Серверы')
    button.filter('Все')

    #sleep(10)
    #assert "Картинки" and "Видео" in elements

# browser = webdriver.Chrome()
# test_yandex_search(browser)