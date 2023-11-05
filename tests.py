import requests
from json import dumps, dump
from os.path import exists
from datetime import datetime

from cookies import save_cookies, load_cookies

from seleniumrequests import Chrome
from selenium.webdriver import ChromeOptions

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

def get_data():
    USERNAME = "asciughino_"

    options = ChromeOptions()

    options.set_capability('goog:loggingPrefs', { 'browser':'ALL' })

    options.add_argument("--headless")

    webdriver = Chrome(options=options)
    webdriver.get("https://www.instagram.com/")
    if exists("cookies/cookies.pkl"):
        for c in load_cookies():
            webdriver.add_cookie(c)
        webdriver.get("https://www.instagram.com/")
    
    _userdata = webdriver.request("GET",f"https://www.instagram.com/web/search/topsearch/?query={USERNAME}")
    userdata = _userdata.json()
    if _userdata.status_code != 200:
        raise ConnectionError(f"({_userdata.status_code}) Could not fetch user data: "+dumps(userdata))

    user_id = userdata["users"][0]["user"]["pk"]
    dump(userdata, open("asciughino.json", "w"), indent=4)

    print(f"Fetching data for user {USERNAME} with id {user_id}")
    
    followers = []
    after = None
    has_next = True
    while has_next:
        url = "https://www.instagram.com/graphql/query/"
        params = {
            "query_hash": "c76146de99bb02f6415203be841dd25a",
            "variables": dumps({
                "id": user_id,
                "include_reel": True,
                "fetch_mutual": True,
                "first": 50,
                "after": after
            })
        }
        response = webdriver.request("GET", url, params=params)
        data = response.json()
        has_next = data["data"]["user"]["edge_followed_by"]["page_info"]["has_next_page"]
        after = data["data"]["user"]["edge_followed_by"]["page_info"]["end_cursor"]
        followers += [
            {
                "username": node["node"]["username"],
                "full_name": node["node"]["full_name"]
            }
            for node in data["data"]["user"]["edge_followed_by"]["edges"]
        ]
    
    print(len(followers))

    after = None
    has_next = True
    followings = []

    while has_next:
        url = "https://www.instagram.com/graphql/query/"
        params = {
            "query_hash": "d04b0a864b4b54837c0d870b0e77e076",
            "variables": dumps({
                "id": user_id,
                "include_reel": True,
                "fetch_mutual": True,
                "first": 50,
                "after": after
            })
        }
        response = webdriver.request("GET", url, params=params)
        data = response.json()
        has_next = data["data"]["user"]["edge_follow"]["page_info"]["has_next_page"]
        after = data["data"]["user"]["edge_follow"]["page_info"]["end_cursor"]
        followings += [
            {
                "username": node["node"]["username"],
                "full_name": node["node"]["full_name"]
            }
            for node in data["data"]["user"]["edge_follow"]["edges"]
        ]

    print(len(followings))

    dont_follow_me_back = [following for following in followings if not any(follower["username"] == following["username"] for follower in followers)]
    i_dont_follow_back = [follower for follower in followers if not any(following["username"] == follower["username"] for following in followings)]

    return ScanData(followers, followings, dont_follow_me_back, i_dont_follow_back)

if __name__ == "__main__":
    scan_data = get_data()
    scan_data.save_to_file()