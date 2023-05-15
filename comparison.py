from os import listdir
import json
from datetime import datetime

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


# Load all results
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

if len(lostFollowers) > 0:
    from web import get_mac_browser,is_user_active
    browser = get_mac_browser()
    for fl in lostFollowers:
        if not is_user_active(browser,fl["username"]):
            fl["status"] = "deactivated"
        else: fl["status"] = "active"

# TODO check if a lost follower has the same bio of a gained follower - it can only have changed account (especially if says deactivated)

# TODO ask the possibility of unfollow lost followers that are still active

print("--------------------------------")
print(f"gained: {str(len(gainedFollowers))}")
print(f"lost: {str(len(lostFollowers))}")
print("--------------------------------")
print("gained followers")
print(gainedFollowers)
print("--------------------------------")
print("lost followers")
print(lostFollowers)

# check if lost followers are really lost follower or deactivated/removed accounts
# from web import get_browser,is_user_active
# browser = get_browser()
# for follower in lostFollowers:
#     if not is_user_active(browser,follower["username"]):
#         print(f"{follower['username']} is deactivated")