import pytest
import time
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException


@pytest.fixture
def driver(request):
    # wd = webdriver.Chrome()
    log_path = "/Users/okamene/dev/bars/geckodriver.log"
    wd = webdriver.Firefox(log_path=log_path)
    # старая схема:
    #wd = webdriver.Firefox(capabilities={"marionette": False})
    # wd = webdriver.Firefox(capabilities={"marionette": True})
    request.addfinalizer(wd.quit)
    return wd

@pytest.fixture
def driver_firefox(request):
    """
    Geckodriver outputs a log.
    :param request:
    :return:
    """
    log_path = "/Users/okamene/dev/bars/geckodriver.log"
    wd = webdriver.Firefox(log_path=log_path)
    # wd = webdriver.Firefox(capabilities={"marionette": False})
    request.addfinalizer(wd.quit)
    return wd


def test_pyth(driver_firefox):
    driver = driver_firefox
    driver.get("http://www.python.org")
    assert "Python" in driver.title



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


