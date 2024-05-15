brew upgrade chromedriver
CHROMEDRIVER_VERSION=$(chromedriver --version | awk {'print $2'})

xattr -d com.apple.quarantine /usr/local/Caskroom/chromedriver/$CHROMEDRIVER_VERSION/chromedriver-mac-x64/chromedriver

