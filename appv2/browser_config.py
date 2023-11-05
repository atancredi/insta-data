from dotenv import load_dotenv
from os import environ as env
# from typing import Any NOSONAR

from selenium.webdriver.remote.webdriver import WebDriver
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities NOSONAR
# from webdriver_manager.chrome import ChromeDriverManager

class Configuration:

    service_path: str
    binary_path: str
    platform: str = "CHROME"
    debug: bool = False

    def __init__(self,
                platform="CHROME",
                service_path="/usr/local/Caskroom/chromedriver/112.0.5615.49/chromedriver",
                binary_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                debug=False,
                from_env=False) -> None:
        
        if from_env:
            load_dotenv()
            self.platform = env.get("PLATFORM")
            self.service_path = env.get("SERVICE_PATH")
            self.binary_path = env.get("BINARY_PATH")
            if env.get("DEBUG") == "True": self.debug = True
            elif env.get("DEBUG") == "False": self.debug = False
            else: self.debug = None
        else:
            self.platform = platform
            self.service_path = service_path
            self.binary_path = binary_path
            self.debug = debug

class BrowserConnector:

    configuration: Configuration
    browser: WebDriver

    def __init__(self, configuration: Configuration = Configuration()) -> None:
        self.configuration = configuration

        options = None
        if self.configuration.platform == "CHROME":
            options = webdriver.ChromeOptions()

            options.set_capability('goog:loggingPrefs', { 'browser':'ALL' })

            options.binary_location = self.configuration.binary_path
            if not self.configuration.debug:
                options.add_argument("--headless")

            service = Service(self.configuration.service_path)
            
            self.browser = webdriver.Chrome(service=service, options=options)

            # if error related to chromedriver
            # brew update
            # brew upgrade --cask chromedriver