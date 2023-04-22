
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.remote.webdriver import WebDriver
from selenium import webdriver

# TODO logging, refactoring
def initialize_browser(debug,platform) -> WebDriver:
    
    options = None
    # Preparation
    if platform == "MAC_OS":
        options = webdriver.ChromeOptions()
        options.binary_location = '/usr/local/Caskroom/chromedriver/89.0.4389.23/chromedriver'
        expath = '/Applications/Brave Browser.app/Contents/MacOS/Brave Browser'
        
    elif platform == "LINUX":
        options = Options()
        options.binary_location = "/usr/lib/firefox/firefox"
    
    if not debug:
        options.add_argument("--headless")
    
    if platform == "MAC_OS":
        return webdriver.Chrome(executable_path=expath, chrome_options=options)
    elif platform == "LINUX":
        return webdriver.Firefox(options=options)
 