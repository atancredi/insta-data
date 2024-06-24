from requests import Session
from utils import execute_request
from json import dumps

from data_models import Follower


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
