from json import dumps
from os.path import exists
from logging import Logger

from cookies_config import load_cookies

from seleniumrequests import Chrome
from selenium.webdriver import ChromeOptions

from data_models import ScanData, Follower

def scan(username: str, logger: Logger):

    options = ChromeOptions()

    options.set_capability('goog:loggingPrefs', { 'browser':'ALL' })

    options.add_argument("--headless")

    webdriver = Chrome(options=options)
    logger.debug("Instantiated Chrome browser")
    webdriver.get("https://www.instagram.com/")
    if exists("cookies/cookies.pkl"):
        logger.debug("Loading cookies")
        for c in load_cookies():
            webdriver.add_cookie(c)
        webdriver.get("https://www.instagram.com/")
    
    _userdata = webdriver.request("GET",f"https://www.instagram.com/web/search/topsearch/?query={username}")
    userdata = _userdata.json()
    if _userdata.status_code != 200:
        raise ConnectionError(f"({_userdata.status_code}) Could not fetch user data: "+dumps(userdata))

    # the first result should be the matching one
    user_id = userdata["users"][0]["user"]["pk"]
    logger.info(f"Found user id {user_id} for user {username}")

    # optionally dump the results of the search
    # dump(userdata, open(f"dump/{username}.json", "w"), indent=4)

    logger.debug(f"Fetching data for user {username} with id {user_id}")
    
    followers: list[Follower] = []
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
            Follower(node["node"])
            for node in data["data"]["user"]["edge_followed_by"]["edges"]
        ]
    
    logger.info(f"Found {len(followers)} followers")

    after = None
    has_next = True
    followings: list[Follower] = []

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
            Follower(node["node"])
            for node in data["data"]["user"]["edge_follow"]["edges"]
        ]

    logger.info(f"Found {len(followings)} followings")

    dont_follow_me_back = [following for following in followings if not any(follower.username == following.username for follower in followers)]
    logger.info(f"Found {len(dont_follow_me_back)} users not following back")
    i_dont_follow_back = [follower for follower in followers if not any(following.username == follower.username for following in followings)]
    logger.info(f"Found {len(i_dont_follow_back)} users not being followed back")

    return ScanData().load_from_raw(followers, followings, dont_follow_me_back, i_dont_follow_back)
