from requests import session
import pickle
from dotenv import load_dotenv
from os import environ as env

from data_models import ScanData
from scan_comparison import ScanComparison
from queries import get_followers, get_following, get_dont_follow_me_back, get_i_dont_follow_back

if __name__ == "__main__":
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

    engine = ScanComparison()
    engine.load_from_files()
    scan_comparison_data = engine.compare_scans()
    scan_comparison_data.save_to_file()
    print("Finished Comparison")
    print(scan_comparison_data.results)

    if len(scan_comparison_data.gained_followers) > 0 or len(scan_comparison_data.lost_followers) > 0:
        scan_res.save_to_file()
        print("Scan results saved to disk")

    print("Finished Scanning")
