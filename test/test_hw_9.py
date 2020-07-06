import pytest
import time
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, InvalidSelectorException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

@pytest.fixture
def driver(request):
    options = Options()
    options.headless = True

    wd = webdriver.Chrome(options=options)
    wd.implicitly_wait(2)
    request.addfinalizer(wd.quit)
    return wd

def test_county_order(driver):
    """
    Test checks if all countries are in alphabetical order
    if country have more than 1 time zone - open country page and check order of time zone
    """
    wait = WebDriverWait(driver, 6)
    ### step 1 - open page, confirm title

    url = 'http://localhost/litecart/admin/?app=countries&doc=countries'
    driver.get(url)


    # login
    username = driver.find_element(By.NAME, 'username')
    password = driver.find_element(By.NAME, 'password')
    submit = driver.find_element(By.NAME, 'login')
    username.send_keys('admin')
    password.send_keys('admin')
    submit.click()

    # verify admin page loaded
    assert 'My Store' in driver.title

    # redirect to Contries page

    driver.find_element_by_xpath("//span[@class='name' and text()='Countries']").click()

    # confirme Countries page is loaded
    assert 'Countries | My Store' in driver.title

    # all rows with countries
    time.sleep(4)
    rows = driver.find_elements_by_class_name("row")
    # create empty list of all countries
    country_list = []
    # create empty list of countries with multiple timezones
    country_zones = []

    for row in rows:
        country = row.find_elements_by_tag_name("td")[4].text
        country_list.append(country)
        tz = int(row.find_elements_by_tag_name("td")[5].text)
        # print(f"Country -> {country}; tz = {tz}")
        if tz > 0:
            el_edit_link = row.find_elements_by_tag_name("td")[4].find_element_by_tag_name("a").get_attribute("href")
            country_zones.append([country, tz, el_edit_link])

    # countries = [row.find_elements_by_tag_name("td")[4].text for row in rows]
    # print(country_zones)

    ### CHECK POINT 1
    # confirm that countries are in alphabetical order
    assert sorted(country_list) == country_list

    ### CHECK POINT 2
    # check countries with multiple time zones
    for country in country_zones:
        # go to the page
        driver.get(country[2])
        # confirm that it is expected page
        expected_name = country[0]
        actual_name = driver.find_element_by_xpath("//input[@name='name']").get_attribute("value")
        assert expected_name == actual_name

        el_all_tz = driver.find_elements_by_xpath("//input[contains(@name, 'name') and @type='hidden']")
        all_tz = [tz.get_attribute("value") for tz in el_all_tz]
        print(all_tz)

        assert sorted(all_tz) == all_tz

