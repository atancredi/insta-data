#TODO spostare dipendenze selenium in web.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

from browsers import initialize_browser

from cookies import save_cookies, load_cookies

from os import environ as env, path
from dotenv import load_dotenv
load_dotenv()
USERNAME = env.get("USR")
PASSWORD = env.get("PSWD")
DEBUG = env.get("DEBUG") or False
PLATFORM = env.get("PLATFORM")


def resolve_cookie_prompt(browser):
    # Cookie screen
    WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.ID,"scrollview")))
    browser.find_element(By.XPATH,"//button[contains(.,'Only allow essential')]").click()

def execute_script(browser,username):
    with open("scripts/script.js") as f:
        _s = f.read()
        print("script loaded")
        # print(_s)

    # inject username
    _s = 'const username = "'+username+'";' + _s    
    retval = browser.execute_async_script(_s)
    print("Done executing script")
    print("retval lenght",str(len(retval)))

    now = datetime.now().strftime("%Y_%m_%d-%H_%M")
    with open("results/result_"+now+".json","w") as f:
        
        f.write(str(retval))


def from_login(browser):
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

    # buttons = browser.find_element(By.TAG_NAME, "button")
    _usr = (By.XPATH,"//input[@name='username']")
    _pwd = (By.XPATH,"//input[@name='password']")
    # __login = browser.find_element(By.XPATH,"//button[contains(.,'Log in')]")
    # print(__login)

    WebDriverWait(browser, 10).until(EC.visibility_of_element_located(_usr))
    browser.find_element(*_usr).clear()
    browser.find_element(*_usr).send_keys(USERNAME)
    browser.find_element(*_pwd).clear()
    browser.find_element(*_pwd).send_keys(PASSWORD)
    browser.find_element(*_pwd).send_keys(Keys.ENTER)
    
    # browser.execute_script("arguments[0].style.display='none'", __login.find_element(By.TAG_NAME,"div"))
    # __login.click()

    WebDriverWait(browser, 10).until(lambda driver: driver.current_url != "https://www.instagram.com/accounts/login/")
    # WebDriverWait(browser,10).until(EC.visibility_of_element_located((By.XPATH,"//button[contains(.,'Save')]")))

    save_cookies(browser)

    return browser

if __name__ == "__main__":
    browser = initialize_browser(PLATFORM)

    browser.get("https://www.instagram.com")
    if path.exists("cookies/cookies.pkl"):
        for c in load_cookies():
            browser.add_cookie(c)
        browser.get("https://www.instagram.com")

    # if no cookies or invalid/expired?
    else:
        from_login(browser)


    execute_script(browser,"asciughino_")
    
    browser.quit()
