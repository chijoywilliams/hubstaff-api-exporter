import os
import json
import time
from pathlib import Path

import requests
from dotenv import load_dotenv


TOKEN_URL = "https://account.hubstaff.com/access_tokens"
USER_INFO_URL = "https://account.hubstaff.com/user_info"
TOKEN_CACHE_FILE = Path(".hubstaff_tokens.json")


def load_cached_tokens():
    if TOKEN_CACHE_FILE.exists():
        with TOKEN_CACHE_FILE.open("r", encoding="utf-8") as file:
            return json.load(file)

    load_dotenv()
    refresh_token = os.getenv("HUBSTAFF_REFRESH_TOKEN")

    if not refresh_token:
        raise RuntimeError("Missing HUBSTAFF_REFRESH_TOKEN in .env file.")

    return {
        "refresh_token": refresh_token,
        "access_token": None,
        "expires_at": 0,
    }


def save_tokens(tokens):
    with TOKEN_CACHE_FILE.open("w", encoding="utf-8") as file:
        json.dump(tokens, file, indent=2)


def refresh_access_token(tokens):
    response = requests.post(
        TOKEN_URL,
        data={
            "grant_type": "refresh_token",
            "refresh_token": tokens["refresh_token"],
        },
        timeout=30,
    )

    if response.status_code != 200:
        raise RuntimeError(
            f"Token refresh failed: {response.status_code} {response.text}"
        )

    data = response.json()

    updated_tokens = {
        "access_token": data["access_token"],
        "refresh_token": data["refresh_token"],
        "expires_at": int(time.time()) + int(data.get("expires_in", 86400)) - 60,
    }

    save_tokens(updated_tokens)
    return updated_tokens


def get_access_token():
    tokens = load_cached_tokens()

    if tokens.get("access_token") and time.time() < tokens.get("expires_at", 0):
        return tokens["access_token"]

    tokens = refresh_access_token(tokens)
    return tokens["access_token"]


def hubstaff_get(url):
    access_token = get_access_token()

    response = requests.get(
        url,
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=30,
    )

    if response.status_code == 401:
        tokens = load_cached_tokens()
        refresh_access_token(tokens)
        access_token = get_access_token()

        response = requests.get(
            url,
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=30,
        )

    if not response.ok:
        raise RuntimeError(
            f"API request failed: {response.status_code} {response.text}"
        )

    return response.json()


if __name__ == "__main__":
    user_info = hubstaff_get(USER_INFO_URL)
    print(json.dumps(user_info, indent=2))
