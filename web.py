from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from datetime import datetime

def get_browser() -> WebDriver:
    # Preparation
    options = Options()
    options.binary_location = "/usr/lib/firefox/firefox"
    
    options.add_argument("--headless")
        
    browser = webdriver.Firefox(options=options)
    return browser


def get_mac_browser():
    driverPath = '/usr/local/Caskroom/chromedriver/89.0.4389.23/chromedriver'
    binaryPath = '/Applications/Brave Browser.app/Contents/MacOS/Brave Browser'
    options = webdriver.ChromeOptions()
    options.binary_location = binaryPath
    browser = webdriver.Chrome(executable_path=driverPath, chrome_options=options)
    return browser


def is_user_active(browser:WebDriver,username:str):
    browser.get("https://www.instagram.com/"+username+"/")
    if "Sorry, this page isn't available." in browser.find_element(By.TAG_NAME,"body").text:
        return False
    return True
