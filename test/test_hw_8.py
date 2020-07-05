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

def test_check_sticker(driver):
    """
    Check every product on HOME page
    Confirm that product has only 1 sticker ( there are several items without stickers )
    1. Find all prodicts
    2. Check each if product has sticket
    3. Assert there is only one ( if any ) sticket
    4. Print out - Product name -> If sticker available -> Which sticker

    """
    wait = WebDriverWait(driver, 6)
    ### step 1 - open page, confirm title

    url = 'http://localhost/litecart/en/'
    driver.get(url)

    # verify admin page loaded
    assert 'Online Store | My Store' in driver.title

    ### step 1 - find all products
    # all products in 3 boxes selectors
    sel_popular = 'box-most-popular'
    sel_campaigns = 'box-campaigns'
    sel_latest = 'box-latest-products'

    # all products boxes elements
    el_popular = driver.find_element(By.ID, sel_popular)
    el_campaigns = driver.find_element(By.ID, sel_campaigns)
    el_latest = driver.find_element(By.ID, sel_latest)

    # function that retrive all products from the box
    def sticker(box):
        all_product = el_popular.find_elements(By.CLASS_NAME, 'product')
        for product in all_product:
            sticker = product.find_elements(By.CLASS_NAME, 'sticker')
            name = product.find_element(By.CLASS_NAME, 'name').text
            if len(sticker) > 0:
                assert len(sticker) == 1
                print(f"Product {name} -- sticker {sticker[0].text} ")
            else:
                print(f"Product {name} -- no sticker")

    sticker(el_popular)
    sticker(el_campaigns)
    sticker(el_latest)
