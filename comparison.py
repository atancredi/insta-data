from os import listdir
import json
from datetime import datetime

# load last 2 results
last2results = []
for file in listdir("results")[-2:]:
    if file.endswith(".json"):
        with open(f"results/{file}", "r") as f:
            last2results.append(json.loads(f.read()))

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

leastRecent = None
mostRecent = None
for i in last2results:

    date = get_date_from_iso(i["date"])
    
    if leastRecent == None:
        leastRecent = i["date"]
    else:
        if date < get_date_from_iso(leastRecent):
            leastRecent = i["date"]
        else:
            if mostRecent == None:
                mostRecent = i["date"]
            elif date > mostRecent:
                mostRecent = i["date"]

# get actual data
leastRecentData = None
mostRecentData = None
for i in last2results:
    if i["date"] == leastRecent:
        leastRecentData = i
    if i["date"] == mostRecent:
        mostRecentData = i

# get gained followers
gainedFollowers = []
for fl in mostRecentData["followers"]:
    if fl["username"] not in [i["username"] for i in leastRecentData["followers"]]:
        gainedFollowers.append(fl)

# get lost followers
lostFollowers = []
for fl in leastRecentData["followers"]:
    if fl["username"] not in [i["username"] for i in mostRecentData["followers"]]:
        lostFollowers.append(fl)

print("--------------------------------")
print(f"gained: {str(len(gainedFollowers))}")
print(f"lost: {str(len(lostFollowers))}")
print("--------------------------------")
print("gained followers")
print(gainedFollowers)
print("--------------------------------")
print("lost followers")
print(lostFollowers)