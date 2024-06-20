from json import dumps
from os.path import exists
from logging import Logger
import asyncio
import pickle
from datetime import datetime

from cookies_config import load_cookies

from seleniumrequests import Chrome
from selenium.webdriver import ChromeOptions, ChromeService

from data_models import ScanData, Follower


def get_webdriver(service_path: str, logger: Logger, headless: True):
    options = ChromeOptions()

    options.set_capability("goog:loggingPrefs", {"browser": "ALL"})

    if headless:
        options.add_argument("--headless")

    service = ChromeService(executable_path=service_path)
    webdriver = Chrome(options=options, service=service)
    logger.debug("Browser Loaded")

    webdriver.get("https://www.instagram.com/")
    if exists("cookies/cookies.pkl"):
        logger.debug("Loading cookies")
        for c in load_cookies():
            webdriver.add_cookie(c)
        webdriver.get("https://www.instagram.com/")
    else:
        print("DO LOGIN!")
        asyncio.run(asyncio.sleep(60))
        pickle.dump(webdriver.get_cookies(), open("cookies/cookies.pkl", "wb"))
        print("cookies saved")

    return webdriver

def get_user_id(username: str, webdriver: Chrome, logger: Logger) -> ScanData:

    username_query = f"https://www.instagram.com/web/search/topsearch/?query={username}"
    logger.debug(f"Searching for username {username} ({username_query})")
    header = {
        "accept": "application/json",
        "accept-encoding": "gzip, deflate",
    }

    user_id = None

    try:
        _userdata = webdriver.request("GET", username_query, header=header)
        userdata = _userdata.json()

        logger.debug("userdata", extra={"userdata": userdata})
        if _userdata.status_code != 200:
            raise ConnectionError(
                f"({_userdata.status_code}) Could not fetch user data: "
                + dumps(userdata)
            )

        # the first result should be the matching one
        user_id = userdata["users"][0]["user"]["pk"]
        logger.info(f"Found user id {user_id} for user {username}")

    except Exception as ex:
        logger.error(f"Could not fetch user data: {ex}")
        with open(f"dumped_requests/{username}_{datetime.now().isoformat()}.html", "w") as f:
            f.write(username_query)
            f.write(_userdata.text)

    # optionally dump the results of the search
    # dump(userdata, open(f"dump/{username}.json", "w"), indent=4)
    if not user_id:
        logger.error(f"Could not find for {user_id}")

    return user_id


def execute_request(webdriver: Chrome, url, logger: Logger, params):
    header = {
        "accept": "application/json",
        "accept-encoding": "gzip, deflate",
    }
    response = webdriver.request("GET", url, headers=header, params=params)
    print("executing request: ",response.url)
    try:
        if response.status_code != 200:
            raise ConnectionError(f"{response.status_code} {response.reason}")
        json = response.json()
        return json

    except Exception as ex:
        logger.error(f"Could not fetch user data: {ex}")
        with open(f"dumped_requests/graphql_request_{datetime.now().isoformat()}.html", "w") as f:
            f.write(url)
            f.write(response.text)

    logger.debug("Unhandled JSON: ", response.text)
    return response.text

def scan(user_id: str, webdriver: Chrome, logger: Logger) -> ScanData:

    logger.debug(f"Fetching data for user {user_id} with id {user_id}")

    followers: list[Follower] = []
    after = None
    has_next = True
    while has_next:
        url = "https://www.instagram.com/graphql/query/"
        params = {
            "query_hash": "c76146de99bb02f6415203be841dd25a",
            "variables": dumps(
                {
                    "id": user_id,
                    "include_reel": True,
                    "fetch_mutual": True,
                    "first": 50,
                    "after": after,
                }
            ),
        }
        data = execute_request(webdriver, url, logger, params=params)
        has_next = data["data"]["user"]["edge_followed_by"]["page_info"][
            "has_next_page"
        ]
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
            "variables": dumps(
                {
                    "id": user_id,
                    "include_reel": True,
                    "fetch_mutual": True,
                    "first": 50,
                    "after": after,
                }
            ),
        }
        data = execute_request(webdriver, url, logger, params=params)
        has_next = data["data"]["user"]["edge_follow"]["page_info"]["has_next_page"]
        after = data["data"]["user"]["edge_follow"]["page_info"]["end_cursor"]
        followings += [
            Follower(node["node"])
            for node in data["data"]["user"]["edge_follow"]["edges"]
        ]

    logger.info(f"Found {len(followings)} followings")

    dont_follow_me_back = [
        following
        for following in followings
        if not any(follower.username == following.username for follower in followers)
    ]
    logger.info(f"Found {len(dont_follow_me_back)} users not following back")
    i_dont_follow_back = [
        follower
        for follower in followers
        if not any(following.username == follower.username for following in followings)
    ]
    logger.info(f"Found {len(i_dont_follow_back)} users not being followed back")

    return ScanData().load_from_raw(
        followers, followings, dont_follow_me_back, i_dont_follow_back
    )
