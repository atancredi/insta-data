
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.remote.webdriver import WebDriver
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# TODO logging, refactoring
def initialize_browser(platform) -> WebDriver:
    
    options = None
    # Preparation
    if platform == "MAC_OS":
        options = webdriver.ChromeOptions()
        service = Service('/usr/local/Caskroom/chromedriver/112.0.5615.49/chromedriver')
        options.binary_location = '/Applications/Brave Browser.app/Contents/MacOS/Brave Browser'
        dc = DesiredCapabilities.CHROME
        dc['goog:loggingPrefs'] = { 'browser':'ALL' }
        return webdriver.Chrome(service=service, chrome_options=options, desired_capabilities=dc)
        
    elif platform == "LINUX":
        options = Options()
        options.binary_location = "/usr/lib/firefox/firefox"
        return webdriver.Firefox(options=options)
