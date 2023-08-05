import requests


def create_review_app(base_url, headers, data):
    url = f"{base_url}/review-apps"

    headers["Content-Type"] = "application/json"

    print("Creating Review app...")
    res = requests.post(url, headers=headers, json=data)
    res.raise_for_status()

    print("Done!")
    response = res.json()

    return response
