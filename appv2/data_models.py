from datetime import datetime
from json import dump

class ScanData:
    followers: list
    followings: list
    dont_follow_me_back: list
    i_dont_follow_back: list
    date: str

    def __init__(self, followers: list, followings: list, dont_follow_me_back: list, i_dont_follow_back: list) -> None:
        self.followers = followers
        self.followings = followings
        self.dont_follow_me_back = dont_follow_me_back
        self.i_dont_follow_back = i_dont_follow_back
       
        self.date = datetime.now().isoformat()
    
    @property
    def __dict__(self):
        return {
            "date": self.date,
            "followers": self.followers,
            "followings": self.followings,
            "dontFollowMeBack": self.dont_follow_me_back,
            "iDontFollowBack": self.i_dont_follow_back,
        }

    def save_to_file(self):
        now = datetime.now().strftime("%Y_%m_%d-%H_%M")
        dump(self.__dict__, open("results/result_"+now+".json","w"), indent=4)
