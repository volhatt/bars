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

def _is_element_present(driver, *args):
    try:
        driver.find_element(*args)
        return True
    except NoSuchElementException:
        return False

def test_adminka(driver):
    """
    Test excecutes 3 steps on the admin menu:
    1. Enter admin panel http://localhost/litecart/admin
    2. Navigates to every page accessable from leftbar menu and sub-menu
    3. Check if header with <h1> exists on the page

    """
    wait = WebDriverWait(driver, 6)
    url = 'http://localhost/litecart/admin'
    driver.get(url)

    ### step 1 - login

    username = driver.find_element(By.NAME, 'username')
    password = driver.find_element(By.NAME, 'password')
    submit = driver.find_element(By.NAME, 'login')
    username.send_keys('admin')
    password.send_keys('admin')
    submit.click()

    # verify admin page loaded
    assert 'My Store' in driver.title

    ### step 2 - check every page
    # create list of Menu items
    all_links = driver.find_elements(By.CSS_SELECTOR, '#box-apps-menu li a')
    menu = [link.text for link in all_links]

    for item in menu:
        sel_menu = f"//span[@class='name' and text()='{item}']"
        button = driver.find_element_by_xpath(sel_menu)
        button.click()
        heading = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'h1')))
        #assert _is_element_present(heading) == True
        assert _is_element_present(driver, By.TAG_NAME, 'h1') == True
        print(f"Menu  {driver.title} heading --> {heading.text}")
        # check if menu item contains sub-menu
        if _is_element_present(driver, By.CSS_SELECTOR, "li#app-.selected ul"):
            sub_menu = driver.find_elements_by_css_selector('li#app-.selected ul a')
            # list of all submenus items
            sub_menu = [link.text for link in sub_menu]
            for item in range(len(sub_menu)):
                el_sub_menus = driver.find_elements_by_css_selector('li#app-.selected ul a')
                el_sub_menus[item].click()
                heading = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'h1')))
                assert _is_element_present(driver, By.TAG_NAME, 'h1') == True
                print(f"--> Sub-menu {driver.title} heading --> {heading.text}")










