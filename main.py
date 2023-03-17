from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

from os import environ as env
from dotenv import load_dotenv
load_dotenv()
USERNAME = "randy_provaprova123"
PASSWORD = env.get("PASSWORD")

def initialize_browser() -> WebDriver:
    
    # Preparation
    options = Options()
    options.binary_location = "/usr/lib/firefox/firefox"
    
    options.add_argument("--headless")
        
    browser = webdriver.Firefox(options=options)
    browser.get("https://www.instagram.com/accounts/login/")

    

    # Cookie screen
    _cs = (By.ID,"scrollview")
    WebDriverWait(browser, 10).until(EC.visibility_of_element_located(_cs))
    browser.find_element(By.XPATH,"//button[contains(.,'Only allow essential')]").click()

    with open("csrf.js","r") as f:
        _s = f.read()
        print(_s)
        browser.execute_script(_s)
    browser.refresh()
    
    # Cookie screen
    WebDriverWait(browser, 10).until(EC.visibility_of_element_located(_cs))
    browser.find_element(By.XPATH,"//button[contains(.,'Only allow essential')]").click()


    # buttons = browser.find_element(By.TAG_NAME, "button")
    _usr = (By.XPATH,"//input[@name='username']")
    _pwd = (By.XPATH,"//input[@name='password']")
    # __login = browser.find_element(By.XPATH,"//button[contains(.,'Log in')]")
    # print(__login)

    WebDriverWait(browser, 10).until(EC.visibility_of_element_located(_usr))
    browser.find_element(*_usr).send_keys(USERNAME)
    browser.find_element(*_pwd).send_keys(PASSWORD)
    browser.find_element(*_pwd).send_keys(Keys.ENTER)
    
    # browser.execute_script("arguments[0].style.display='none'", __login.find_element(By.TAG_NAME,"div"))
    # __login.click()

    WebDriverWait(browser, 10).until(lambda driver: driver.current_url != "https://www.instagram.com/accounts/login/")
    WebDriverWait(browser,10).until(EC.visibility_of_element_located((By.XPATH,"//button[contains(.,'Save')]")))

    with open("script.js") as f:
        _s = f.read()
        print("script loaded")
        # print(_s)
    
    retval = browser.execute_async_script(_s)
    print("Done executing script")
    # print(retval)

    now = datetime.now().strftime("%Y_%m_%d-%H_%M")
    with open("results/result_"+now+".json","w") as f:
        
        f.write(str(retval))

    return browser


if __name__ == "__main__":
    initialize_browser()