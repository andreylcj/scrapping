from typing import Union, List
from selenium import webdriver
import logging
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
from selenium.webdriver.chrome.webdriver import WebDriver

GOOGLE = 'GOOGLE'
CHROMIUM = 'CHROMIUM'
BRAVE = 'BRAVE'
MSEDGE = 'MSEDGE'


def chrome_start(
    chrome_type: Union[
        GOOGLE, CHROMIUM, BRAVE, MSEDGE
    ]=GOOGLE,
    chrome_options_arguments: List[str]=[],
    warning_logs: bool=True,
    load_images: bool=False,
    load_js: bool=True,
) -> WebDriver:
        
    
    # Only display possible problems
    if warning_logs:
        logging.getLogger('selenium.webdriver.remote.remote_connection') \
            .setLevel(logging.WARNING)
        logging.getLogger('urllib3.connectionpool') \
            .setLevel(logging.WARNING)

    chrome_options = webdriver.ChromeOptions()

    # chrome options arguments
    for arg in chrome_options_arguments:
        chrome_options.add_argument(arg)
        
    # remove UI
    """ chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--mute-audio')
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--window-size=1920x1080") """

    ### This blocks images and javascript requests
    chrome_prefs = { "profile.default_content_setting_values": {} }
    
    if not load_images:
        chrome_prefs['profile.default_content_setting_values']['images'] = 2
    if not load_js:
        chrome_prefs['profile.default_content_setting_values']['javascript'] = 2

    chrome_options.experimental_options["prefs"] = chrome_prefs
    ###

    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager(
            chrome_type=getattr(ChromeType, chrome_type)
            ).install()),
        chrome_options=chrome_options
    )
    
    return driver