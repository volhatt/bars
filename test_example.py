import pytest
import time
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    request.addfinalizer(wd.quit)
    return wd


def test_example(driver):
    driver.get('https://www.google.com/')
    driver.find_element_by_name('q').send_keys('webdriver')
    # test failed without pause
    time.sleep(1)
    driver.find_element_by_name('btnK').click()
    time.sleep(1)
    WebDriverWait(driver, 10).until(EC.title_is('webdriver - Google Search'))


def test_admin(driver):
    driver.get('http://localhost/litecart/admin/')
    driver.find_element_by_name('username').send_keys('admin')
    driver.find_element_by_name('password').send_keys('admin')
    driver.find_element_by_name('remember_me').click()
    driver.find_element_by_name('login').click()
    # time.sleep(10)


