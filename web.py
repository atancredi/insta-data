from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

def get_browser() -> WebDriver:
    # Preparation
    options = Options()
    options.binary_location = "/usr/lib/firefox/firefox"
    
    options.add_argument("--headless")
        
    browser = webdriver.Firefox(options=options)
    return browser

def is_user_active(browser:WebDriver,username:str):
    browser.get("https://www.instagram.com/"+username+"/")
    if "Sorry, this page isn't available." in browser.find_element(By.TAG_NAME,"body").text:
        return False
    return True
