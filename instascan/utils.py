from requests import Session
from datetime import datetime

def execute_request(session: Session, url, params):
    header = {
        "accept": "application/json",
        "accept-encoding": "gzip, deflate",
    }
    response = session.get(url, headers=header, params=params)
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

