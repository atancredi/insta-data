#TODO spostare dipendenze selenium in web.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from browsers import BrowserConnector, Configuration
from cookies import save_cookies, load_cookies
from selenium.webdriver.remote.webdriver import WebDriver
from os import environ as env, path
from dotenv import load_dotenv

# TODO watch log console from js
def watch_log(browser):
    for log in browser.get_log('browser'): print(log)

def resolve_cookie_prompt(browser):
    # Cookie screen
    WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.ID,"scrollview")))
    browser.find_element(By.XPATH,"//button[contains(.,'Only allow essential')]").click()

def execute_script(browser:WebDriver,username:str):
    with open("scripts/script.js") as f:
        _s = f.read()
        print("script loaded")

    # inject username
    _s = 'const username = "'+username+'";' + _s    
    retval = browser.execute_async_script(_s)
    print("Done executing script")
    print("retval lenght",str(len(retval)))
    now = datetime.now().strftime("%Y_%m_%d-%H_%M")
    with open("results/result_"+now+".json","w") as f:
        f.write(str(retval))

def from_login(browser:WebDriver,username,password):
    browser.get("https://www.instagram.com/accounts/login/")

    # Cookie screen
    resolve_cookie_prompt(browser)

    with open("scripts/csrf.js","r") as f:
        _s = f.read()
        print(_s)
        browser.execute_script(_s)
    browser.refresh()
    
    # Cookie screen
    resolve_cookie_prompt(browser)

    _usr = (By.XPATH,"//input[@name='username']")
    _pwd = (By.XPATH,"//input[@name='password']")

    WebDriverWait(browser, 10).until(EC.visibility_of_element_located(_usr))
    browser.find_element(*_usr).clear()
    browser.find_element(*_usr).send_keys(username)
    browser.find_element(*_pwd).clear()
    browser.find_element(*_pwd).send_keys(password)
    browser.find_element(*_pwd).send_keys(Keys.ENTER)
    
    WebDriverWait(browser, 10).until(lambda driver: driver.current_url != "https://www.instagram.com/accounts/login/")

    save_cookies(browser)

    return browser

def scan():

    load_dotenv()
    USERNAME = env.get("USR")
    PASSWORD = env.get("PSWD")

    conf = Configuration(from_env=True)
    b = BrowserConnector(conf)
    browser = b.browser

    browser.get("https://www.instagram.com")
    if path.exists("cookies/cookies.pkl"):
        for c in load_cookies():
            browser.add_cookie(c)
        browser.get("https://www.instagram.com")

    # if no cookies or invalid/expired?
    else:
        from_login(browser,USERNAME,PASSWORD)

    execute_script(browser,"asciughino_")
    
    browser.quit()
