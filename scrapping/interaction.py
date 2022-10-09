from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
import logging
from selenium.webdriver.chrome.webdriver import WebDriver


def wait_for_element(
    driver: WebDriver, 
    expected_conditions: EC, 
    delay: int=5, 
    verbose: bool=True
) -> WebDriver:
    # expected_conditions = EC.presence_of_element_located((By.ID, 'IdOfMyElement'))
    my_elem = None
    try:
        my_elem = WebDriverWait(driver, delay).until(expected_conditions)
        if verbose:
            logging.debug("Expected conditions were satisfied!")
    except TimeoutException:
        raise TimeoutException("Expected conditions took too much time!")
    return my_elem


def open_tab(
    driver: WebDriver, 
    url: str='',
    js: bool=True
) -> WebDriver:
    try:
        driver.execute_script(f'window.open("{url}","_blank");')
        got_to_tab(driver, -1)
    except:
        got_to_tab(driver, 0)
        driver.execute_script(f'window.open("{url}","_blank");')
        got_to_tab(driver, -1)
    return driver


def got_to_tab(
    driver: WebDriver, 
    tab_index: int=0
) -> WebDriver:
    driver.switch_to.window(driver.window_handles[tab_index])
    return driver


def go_to_page(
    driver: WebDriver, 
    url: str
) -> WebDriver:
    driver.get(url)
    return driver


def find_element(
    query: str, 
    driver: WebDriver=None , 
    reference_el: any=None, 
    by: By=By.XPATH, 
    verbose: bool=False
) -> any:
    result = None
    try:
        if reference_el is not None:
            result = reference_el.find_element(by, value=query)
        elif driver is not None:
            result = driver.find_element(by, value=query)
        else:
            raise Exception('Provide "driver" or "reference_el".')
    except Exception as exc:
        if verbose:
            print(exc.msg)
        result = None
    return result


def find_elements(
    query: str, 
    driver: WebDriver=None, 
    reference_el: any=None, 
    by: By=By.XPATH,
    verbose: bool=False
) -> any:
    result = None
    try:
        if reference_el is not None:
            result = reference_el.find_elements(by, value=query)
        elif driver is not None:
            result = driver.find_elements(by, value=query)
        else:
            raise Exception('Provide "driver" or "reference_el".')
    except Exception as exc:
        if verbose:
            print(exc.msg)
        result = None
    return result


def perform_click(
    element,
    driver: WebDriver=None,
    js: bool=False
) -> None:
    if js:
        driver.execute_script("arguments[0].click();", element)
    else:
        element.click()


def click(
    element: any, 
    driver: WebDriver=None, 
    retry: int=5, 
    js: bool=True, 
    js_when_exaust: bool=True, 
    verbose: bool=False
) -> None:
    if js:
        assert driver is not None, 'When "js" == True, you need provide "driver"'
    retry_count = 0
    while retry_count < retry:
        try:
            perform_click(element, driver, js)
            retry_count = float('inf')
        except Exception as exc:
            retry_count = retry_count + 1
            msg = exc
            if verbose:
                print(f'retry: {retry_count}')
                print(msg)
    if retry_count != float('inf'):
        if js_when_exaust and driver is not None:
            perform_click(element, driver, js=True)
        else:
            raise Exception(msg)


def set_input_range_value(
    input_el: any, 
    driver: WebDriver, 
    value: int
) -> webdriver:
    curr_val = int(input_el.get_attribute('value'))
    is_right_key = value > curr_val
    if is_right_key:        
        max_val = int(input_el.get_attribute('max'))
        max_val = max(value, max_val)
        for i in range(max_val - curr_val):
            input_el.send_keys(Keys.RIGHT)
    else:
        min_val = int(input_el.get_attribute('min'))
        min_val = min(value, min_val)
        for i in range(curr_val, min_val, -1):
            input_el.send_keys(Keys.LEFT)
    return driver


def get_el_on_el_list(xpath):
    """get xpath value that represent list, yield first el and increase
    by 1 iterator num"""
    pass