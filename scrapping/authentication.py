from selenium.webdriver.common.by import By
from scrapping.interaction import click
from selenium import webdriver


def auto_login(
    driver: webdriver, 
    username: str, 
    password: str
) -> webdriver:
    # Find a password input field and enter the specified password string
    password_xpath = "//input[@type='password']"
    # password_input = wait_for_element(driver, EC.presence_of_element_located((By.XPATH, password_xpath)))
    password_input = driver.find_element(by=By.XPATH, value=password_xpath)
    # driver.execute_script(f"arguments[0].value = \"{password}\";", password_input)
    password_input.send_keys(password)

    # Find a visible input field preceding out password field and enter the specified username
    # username_abs_xpath = f"{password_xpath}/preceding::input[not(@type='hidden')][1]"
    # username_input = wait_for_element(driver, EC.presence_of_element_located((By.XPATH, username_abs_xpath)))
    username_xpath = "preceding::input[not(@type='hidden')][1]"
    username_input = password_input.find_element(by=By.XPATH, value=username_xpath)
    # driver.execute_script(f"arguments[0].value = \"{username}\";", username_input)
    username_input.send_keys(username)

    # Find the form element enclosing our password field
    form_element = password_input.find_element(by=By.XPATH, value=".//ancestor::form")

    # Find the form's submit element and click it
    submit_button = form_element.find_element(by=By.XPATH, value=".//*[@type='submit']")
    click(submit_button, driver=driver)

    return driver