from requests import session, Session
import pickle
from datetime import datetime
from json import dumps
from dotenv import load_dotenv
from os import environ as env

from app.data_models import ScanData, Follower


def execute_request(session: Session, url, params):
    header = {
        "accept": "application/json",
        "accept-encoding": "gzip, deflate",
    }
    response = session.get(url, headers=header, params=params)
    # print(f"executed request with status code {response.status_code}")
    # print(response.url)
    try:
        if response.status_code != 200:
            raise ConnectionError(f"{response.status_code} {response.reason}")
        json = response.json()
        return json

    except Exception as ex:
        print(f"Could not fetch user data: {ex}")
        with open(
            f"dumped_requests/graphql_request_{datetime.now().isoformat()}.html", "w"
        ) as f:
            f.write(url)
            f.write(response.text)

    print("Unhandled JSON: ", response.text)
    return response.text


def get_followers(user_id, sex: Session):
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
        data = execute_request(sex, url, params=params)
        has_next = data["data"]["user"]["edge_followed_by"]["page_info"][
            "has_next_page"
        ]
        after = data["data"]["user"]["edge_followed_by"]["page_info"]["end_cursor"]
        followers += [
            Follower(node["node"])
            for node in data["data"]["user"]["edge_followed_by"]["edges"]
        ]
    return followers


def get_following(user_id, sex: Session):
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
        data = execute_request(sex, url, params=params)
        has_next = data["data"]["user"]["edge_follow"]["page_info"]["has_next_page"]
        after = data["data"]["user"]["edge_follow"]["page_info"]["end_cursor"]
        followings += [
            Follower(node["node"])
            for node in data["data"]["user"]["edge_follow"]["edges"]
        ]
    return followings


def get_dont_follow_me_back(followings, followers):
    return [
        following
        for following in followings
        if not any(follower.username == following.username for follower in followers)
    ]


def get_i_dont_follow_back(followings, followers):
    return [
        follower
        for follower in followers
        if not any(following.username == follower.username for following in followings)
    ]


pk = pickle.load(open("cookies/cookies.pkl", "rb"))


sex = session()
for cookie in pk:
    sanified_cookie = {}
    sanified_cookie["value"] = cookie["value"]
    if isinstance(cookie["value"], bytes):
        sanified_cookie["value"] = cookie["value"].decode("utf-8")
    sex.cookies.set(
        cookie["name"], sanified_cookie["value"].replace("b'", "").replace("'", "")
    )

load_dotenv()
user_id = env.get("USER_ID")
print(f"Fetching data for user {user_id}")

followers = get_followers(user_id, sex)
print(f"Found {len(followers)} followers")

followings = get_following(user_id, sex)
print(f"Found {len(followings)} followings")

dont_follow_me_back = get_dont_follow_me_back(followings, followers)
print(f"Found {len(dont_follow_me_back)} users not following back")

i_dont_follow_back = get_i_dont_follow_back(followings, followers)
print(f"Found {len(i_dont_follow_back)} users not being followed back")

scan_res = ScanData()
scan_res.load_from_raw(followers, followings, dont_follow_me_back, i_dont_follow_back)
scan_res.save_to_file()

