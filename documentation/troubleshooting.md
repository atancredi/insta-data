## Troubleshooting
IF selenium.common.exceptions.SessionNotCreatedException: Message: session not created: This version of ChromeDriver only supports Chrome version ...
- run this command - brew upgrade chromedriver
-  run - xattr -d com.apple.quarantine /usr/local/Caskroom/chromedriver/120.0.6099.109/chromedriver-mac-x64/chromedriver

IF selenium cannot find the driver update it and reference the right service path in the env file
