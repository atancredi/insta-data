from os import listdir
import json
from datetime import datetime
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By

from engine import Configuration, BrowserConnector

def is_user_active(browser:WebDriver,username:str):
    browser.get("https://www.instagram.com/"+username+"/")
    if "Sorry, this page isn't available." in browser.find_element(By.TAG_NAME,"body").text:
        return False
    return True

# get least and most recent results
def get_date_from_iso(iso):
    if type(iso).__name__ == "datetime" or "T" not in iso:
        return iso

    _ = iso.split("T")
    __ = _[0].split("-")
    year = __[0]
    month = __[1]
    day = __[2]
    __ = _[1].split(":")
    hour = __[0]
    minute = __[1]
    return datetime(int(year), int(month), int(day), int(hour), int(minute))

# Load all results - TODO THIS HAS NO SENSE, AS THE FILE INCREASES THIS BECOMES MESSY
resultsData = []
for file in listdir("results"):
    if file.endswith(".json") and not file.startswith("_"):
        with open(f"results/{file}", "r") as f:
            resultsData.append(json.loads(f.read()))

# Sort by date
resultsData.sort(key=lambda x: get_date_from_iso(x["date"]), reverse=False)

# get actual data from most recent and 2nd most recent scan
leastRecentData = resultsData[-2]
mostRecentData = resultsData[-1]

# get gained followers
gainedFollowers = []
for fl in mostRecentData["followers"]:
    if fl["username"] not in [i["username"] for i in leastRecentData["followers"]]:
        gainedFollowers.append(fl)

# get lost followers
# check if lost followers are really lost follower or deactivated/removed accounts

lostFollowers = []
for fl in leastRecentData["followers"]:
    if fl["username"] not in [i["username"] for i in mostRecentData["followers"]]:
        lostFollowers.append(fl)

conf = Configuration(from_env=True)
b = BrowserConnector(conf)
browser = b.browser
if len(lostFollowers) > 0:
    for fl in lostFollowers:
        if not is_user_active(browser,fl["username"]):
            fl["status"] = "deactivated"
        else: fl["status"] = "active"

# TODO check if a lost follower has the same bio of a gained follower - it can only have changed account (especially if says deactivated)  NOSONAR

# TODO ask the possibility of unfollow lost followers that are still active  NOSONAR

# TODO lost follower status - to enum NOSONAR

print("--------------------------------")
print(f"gained: {str(len(gainedFollowers))}")
print(f"lost: {str(len(lostFollowers))}")
print("--------------------------------")
print("gained followers")
print(gainedFollowers)
print("--------------------------------")
print("lost followers - deactivated")
print([x for x in lostFollowers if x["status"] == "deactivated"])
print("--------------------------------")
print("lost followers - active")
print([x for x in lostFollowers if x["status"] == "active"])

# check if lost followers are really lost follower or deactivated/removed accounts
# from web import get_browser,is_user_active
# browser = get_browser()
# for follower in lostFollowers:
#     if not is_user_active(browser,follower["username"]):
#         print(f"{follower['username']} is deactivated")