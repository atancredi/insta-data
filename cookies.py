import pickle

# TODO logging
def save_cookies(browser):
    pickle.dump(browser.get_cookies(), open("cookies/cookies.pkl", "wb"))
    print("cookies saved")

def load_cookies():
    with open("cookies/cookies.pkl", "rb") as f:
        return pickle.load(f)
    