from datetime import datetime
from typing import List, Optional
from datetime import datetime
from json import dump

def get_date_from_iso(iso: str | datetime):
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

class Follower:
    username: str
    full_name: str
    
    @property
    def __dict__(self):
        return {
            "username": self.username,
            "full_name": self.full_name
        }
    
    def __init__(self,object: dict):
        self.username=object["username"]
        self.full_name=object["full_name"]

class ScanData:
    followers: List[Follower]
    followings: List[Follower]
    dont_follow_me_back: List[Follower]
    i_dont_follow_back: List[Follower]
    date: datetime

    def set_date(self,date):
        if not date:
            self.date = datetime.now()
        elif isinstance(date, str):
            self.date = get_date_from_iso(date)
        elif isinstance(date, datetime):
            self.date = date

    def load_from_raw(self, followers: List[Follower], followings: List[Follower], dont_follow_me_back: List[Follower], i_dont_follow_back: List[Follower], date: Optional[datetime] = None) -> None:
        self.set_date(date)
        self.followers = followers
        self.followings = followings
        self.dont_follow_me_back = dont_follow_me_back
        self.i_dont_follow_back = i_dont_follow_back
        return self
        
    def load_from_dict(self, object: dict):
        self.set_date(object["date"])
        self.followers = [Follower(x) for x in object["followers"]]
        self.followings = [Follower(x) for x in object["followings"]]
        self.dont_follow_me_back = [Follower(x) for x in object["dont_follow_me_back"]]
        self.i_dont_follow_back = [Follower(x) for x in object["i_dont_follow_back"]]
        return self

    @property
    def __dict__(self):
        return {
            "followers": [follower.__dict__ for follower in self.followers],
            "followings": [follower.__dict__ for follower in self.followings],
            "dont_follow_me_back": [follower.__dict__ for follower in self.dont_follow_me_back],
            "i_dont_follow_back": [follower.__dict__ for follower in self.i_dont_follow_back],
            "date": self.date.isoformat(),
        }

    def save_to_file(self):
        now = self.date.strftime("%Y_%m_%d-%H_%M")
        dump(self.__dict__, open("results/result_"+now+".json","w"), indent=4)

class TimeObject:
    reference_scan: datetime
    current_scan: datetime

    def __init__(self, reference_scan: datetime, current_scan: datetime) -> None:
        self.reference_scan = reference_scan
        self.current_scan = current_scan

class ProfileData(Follower):
    
    def __init__(self,object: dict) -> None:
        super().__init__(object)
    
class ScanComparisonData:

    time_object: TimeObject
    profile_data: ProfileData
    gained_followers: List[Follower]
    lost_followers: List[Follower]

    @property
    def __dict__(self):
        return {
            "time_object": {
                "reference_scan": self.time_object.reference_scan.isoformat(),
                "current_scan": self.time_object.current_scan.isoformat()
            },
            "gained_followers": [x.__dict__ for x in self.gained_followers],
            "lost_followers": [x.__dict__ for x in self.lost_followers],
        }

    def save_to_file(self):
        d = datetime.now().strftime("%Y_%m_%d-%H_%M")
        dump(self.__dict__, open("results_comparisons/result_"+d+".json","w"), indent=4)
